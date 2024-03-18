import json
import lucene
import os
import sys
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer, SimpleAnalyzer, WhitespaceAnalyzer
from org.apache.lucene.document import Document, StringField, TextField, IntPoint, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.util import BytesRef

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        post_data = json.load(file)
    return post_data

def get_analyzer(analyzer_name):
    if analyzer_name == "StandardAnalyzer":
        return StandardAnalyzer()
    elif analyzer_name == "KeywordAnalyzer":
        return KeywordAnalyzer()
    elif analyzer_name == "SimpleAnalyzer":
        return SimpleAnalyzer()
    elif analyzer_name == "WhitespaceAnalyzer":
        return WhitespaceAnalyzer()
    else:
        print("Invalid analyzer option. Using StandardAnalyzer by default.")
        return StandardAnalyzer()

def document_exists(directory, url):
    try:
        reader = DirectoryReader.open(directory)
        searcher = IndexSearcher(reader)
        query = TermQuery(Term("url", url))
        top_docs = searcher.search(query, 1)
        return top_docs.totalHits.value > 0
    except Exception as e:
        print(f"Error checking document existence: {e}")
        return False
    finally:
        if 'reader' in locals():
            reader.close()

def create_index(index_path, posts, analyzer_name):
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    directory = SimpleFSDirectory.open(Paths.get(index_path))
    analyzer = get_analyzer(analyzer_name)
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(directory, config)

    for post in posts:
        url = post.get("URL", "")
        if not document_exists(directory, url):
            doc = Document()
            doc.add(TextField("title", post.get("Title", ""), StoredField.Store.YES))
            doc.add(StringField("url", url, StoredField.Store.YES))
            doc.add(IntPoint("score", post.get("Score", 0)))
            doc.add(StoredField("score", post.get("Score", 0)))
            createdAt = str(post.get("CreatedAt", ""))
            doc.add(StringField("createdAt", createdAt, StoredField.Store.YES))
            doc.add(TextField("content", post.get("Full Content", ""), StoredField.Store.YES))
            writer.addDocument(doc)

    writer.commit()
    writer.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_directory> <analyzer>")
        sys.exit(1)

    d_path = sys.argv[1]
    analyzer_name = sys.argv[2]
    base_path = d_path
    json_file_path = os.path.join(base_path, d_path+'reddit_posts.json')
    index_path = os.path.join(base_path, 'lucene_index/')

    if not os.path.exists(index_path):
        os.makedirs(index_path)

    posts = read_json_file(json_file_path)
    create_index(index_path, posts, analyzer_name)
    print("Indexing completed successfully.")

