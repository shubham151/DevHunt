import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory

def search_documents(index_path, query_str):
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    directory = SimpleFSDirectory.open(Paths.get(index_path))
    reader = DirectoryReader.open(directory)
    searcher = IndexSearcher(reader)

    analyzer = StandardAnalyzer()
    query_parser = QueryParser("content", analyzer)
    query = query_parser.parse(query_str)

    top_docs = searcher.search(query, 10)

    # Print search results
    print("---------------------------------------------------------------------------------------------")
    print(f"Found {top_docs.totalHits.value} result(s) for query: '{query_str}':")
    print("---------------------------------------------------------------------------------------------")
    for score_doc in top_docs.scoreDocs:
        doc = searcher.doc(score_doc.doc)
        print(f"Document {score_doc.doc} | Score: {score_doc.score}")
        print(f"Title: {doc.get('title')}")
        print(f"URL: {doc.get('url')}")
        print(f"CreatedAt: {doc.get('createdAt')}")
        print(f"Content: {doc.get('content')[:200]}...")
        print('______________________________________________________________/n')

    # Close resources
    reader.close()
    directory.close()

if __name__ == "__main__":
    index_path = './lucene_index'
    query_str = input("Enter your search query: ")
    search_documents(index_path, query_str)

