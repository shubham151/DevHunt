from flask import Flask, render_template, request, flash
from bert_indexing import search
from pylucene_indexing import reddit_search 
from code_generator import code_snippet as code_snippet_file

app = Flask(__name__)

app.config['SECRET_KEY'] = 'INFO_RETRIEVAL_PROJECT_GROUP_11'

programming_language_results = [
    # {
    #   "title":"Kabsch-Umeyama Algorithm - How to Align Point Patterns",
    #   "score": 4,
    #   "comments": 0,
    #   "created_at": "2023-12-02 02:58:52"
    # }
]

other_results = []


@app.route("/", methods=["GET", "POST"])
def index():
    global programming_language_results, other_results
    required_keys = {"title", "url", "score", "content"}
    programming_language_results = []
    other_results = []
    query = ''
    indexing_type = ''
    programming_language = ''
    data = request.form
    code_snippet = ''
    explanation = ''
    if request.method == 'POST':
        query = str(data.get('query-input'))
        indexing_type = str(data.get('searchOption'))
        programming_language = str(data.get('programming-language'))
        if indexing_type == 'bert':
            programming_language_results, other_results = search.search_and_return(
                query, programming_language)
            for result in programming_language_results:
                result["content"] = max(
                    result["Comments"], key=lambda x: x['Score'])["Comment"]
                result["title"] = result["Title"]
                result["score"] = result["Score"]
                result["url"] = result["URL"]
            for result in other_results:
                result["content"] = max(
                    result["Comments"], key=lambda x: x['Score'])["Comment"]
                result["title"] = result["Title"]
                result["score"] = result["Score"]
                result["url"] = result["URL"]

            programming_language_results = [{key: x[key] for key in x.keys() & required_keys} for x in programming_language_results]
            other_results = [{key: x[key] for key in x.keys() & required_keys}
                             for x in other_results]
        elif indexing_type == 'pylucene':
            modified_query = programming_language + " " + query
            programming_language_results = reddit_search.search_amd_return_docs(modified_query)
            print(" ")
        
        code_snippet,explanation = code_snippet_file.generate_code_and_explanation(programming_language + " " + query)
        if explanation == "No explanation available.":
            explanation = ''
    return render_template("index.html", results=programming_language_results, other_results=other_results, query=query, indexing_type=indexing_type.capitalize(), programming_language=programming_language.capitalize(), code_snippet = code_snippet, explanation = explanation)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
