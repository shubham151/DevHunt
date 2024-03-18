import json
import lucene
import os
import sys
from java.nio.file import Paths
import json
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import faiss
import re  # For extracting subreddit names from URLs
import tqdm  # For progress tracking

MAX_LEN=512
# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        post_data = json.load(file)
    return post_data

# Function to get BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=MAX_LEN, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:,0,:].cpu().numpy()  # Use the [CLS] token's embedding
    return embeddings

# Adjusted function to extract subreddit name from URL or mark as "UNKNOWN URL"
def extract_subreddit(url):
    if not url:  # Check if URL is None or empty
        return "UNKNOWN_URL"  # Return a distinct placeholder for missing URLs
    match = re.search(r"reddit\.com/r/([^/]+)/", url)
    return match.group(1) if match else "UNKNOWN_URL"

# Update the data to include subreddit information, handling missing URLs
def handle_missing_key(posts):
    for post in posts:
        post["Subreddit"] = extract_subreddit(post.get("URL", None))
    return posts

# Function to process data in batches and get embeddings, with a smaller batch size of 10
def process_data_in_batches(data, batch_size=10):
    embeddings_list = []
    for i in tqdm.tqdm(range(0, len(data), batch_size), desc="Processing posts"):
        batch = data[i:i+batch_size]
        batch_embeddings = np.vstack([get_bert_embedding(post["Full Content"]) for post in batch])
        embeddings_list.append(batch_embeddings)
    return np.vstack(embeddings_list)

# Process data and collect embeddings with the specified batch size
def create_index(inp_path, out_path, data):

    embeddings = process_data_in_batches(data)

    # Initialize and populate FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save the index to disk
    faiss.write_index(index, out_path+"reddit_posts.index")

    # Save the updated data (including subreddit info) to disk
    with open(out_path+"reddit_posts_order_with_subreddit.json", "w") as file:
        json.dump(data, file)

if __name__ == "__main__":
    inp_path = sys.argv[1]
    out_path = sys.argv[2]
    
    json_file_path = os.path.join(inp_path, 'reddit_posts.json')
    index_path = os.path.join(out_path, 'index/')

    if not os.path.exists(index_path):
        os.makedirs(index_path)
    posts = read_json_file(json_file_path)
    posts = handle_missing_key(posts)

    create_index(inp_path, index_path, posts)
    print("Indexing completed successfully.")
