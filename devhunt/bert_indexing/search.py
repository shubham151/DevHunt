import json
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import faiss
import datetime
from static import constants

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Load the FAISS index
index = faiss.read_index(constants.path_to_bert_indexing + "/reddit_posts.index")

# Load the data
with open(constants.path_to_bert_indexing +"/reddit_posts_order_with_subreddit.json", "r") as file:
    data = json.load(file)

# Function to get BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:,0,:].cpu().numpy()  # Use the [CLS] token's embedding
    return embeddings

# Function to search and display results
def search_and_display(query, programming_language):
    # Get the query embedding
    query_embedding = get_bert_embedding(query)
    
    # Search in the FAISS index
    D, I = index.search(query_embedding, k=10)  # For example, search for top 10 similar posts
    
    programming_language_results = []
    other_results = []
    
    # Filter results based on programming language
    for idx in I[0]:
        post = data[idx]
        if programming_language.lower() in post["URL"].lower():
            programming_language_results.append(post)
        else:
            other_results.append(post)
    
    # Display results for the specified programming language
    print(f"\nResults for programming language {programming_language}:")
    for post in programming_language_results:
        print_result(post)

    print("\nOther results:")
    for post in other_results:
        print_result(post)

def print_result(post):
    created_at = datetime.datetime.fromtimestamp(post.get('CreatedAt')).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\nTitle: {post.get('Title')}\nScore: {post.get('Score')}\nComments: {post.get('CntComments', 'N/A')}\nCreated At: {created_at}")

# Function to search and return results
def search_and_return(query, programming_language):
    # Get the query embedding
    query_embedding = get_bert_embedding(query)
    
    # Search in the FAISS index
    D, I = index.search(query_embedding, k=10)  # For example, search for top 10 similar posts
    
    programming_language_results = []
    other_results = []
    
    # Filter results based on programming language
    for idx in I[0]:
        post = data[idx]
        if programming_language.lower() in post["URL"].lower():
            programming_language_results.append(post)
        else:
            other_results.append(post)
    return programming_language_results, other_results

# Example usage
if __name__ == "__main__":
    print("LOADING DEVHUNT.......")
    # Load BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Load the FAISS index
    index = faiss.read_index("reddit_posts.index")

    # Load the data
    with open("reddit_posts_order_with_subreddit.json", "r") as file:
        data = json.load(file)
    q=True
    while(q):
        print("______________________________________________")
        query = input("Enter your search query or press q for exit: ")
        if query == 'q':
            q=False
            continue
        programming_language = input("Enter the programming language: ")
        search_and_display(query, programming_language)

    print("---------------------CLOSED--------------")
