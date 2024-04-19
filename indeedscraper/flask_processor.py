from flask import Flask, request, jsonify
import pickle
import math
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

# Load inverted index from pickle file
def load_inverted_index(index_filename):
    with open(index_filename, 'rb') as f:
        inverted_index = pickle.load(f)
    return inverted_index

# Load stop words for text preprocessing
stop_words = set(stopwords.words('english'))

# Function to preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]  # Remove stop words
    return ' '.join(tokens)

# Function to perform query processing
def process_query(query, inverted_index, total_docs, k=5):
    query = preprocess_text(query)
    query_terms = query.split()
    
    # Calculate TF-IDF scores for query terms
    query_tfidf = defaultdict(float)
    for term in query_terms:
        if term in inverted_index:
            df = len(inverted_index[term])  # Document frequency (DF)
            idf = math.log10(total_docs / df) if df != 0 else 0  # Inverse Document Frequency (IDF)
            tfidf_query_term = (query_terms.count(term) / len(query_terms)) * idf  # TF-IDF for query term
            query_tfidf[term] = tfidf_query_term
    
    # Rank documents based on cosine similarity with query
    ranked_results = defaultdict(float)
    for term, tfidf_query_term in query_tfidf.items():
        for doc_id, tfidf_doc_term in inverted_index[term]:
            ranked_results[doc_id] += tfidf_query_term * tfidf_doc_term
    
    # Sort and get top-K results
    top_results = sorted(ranked_results.items(), key=lambda x: x[1], reverse=True)[:k]
    return top_results

@app.route('/query', methods=['GET', 'POST'])
def query():
    global inverted_index, total_docs  # Access global variables
    
    if request.method == 'POST':
        data = request.get_json()
        if 'query' not in data:
            return jsonify({'error': 'Query field is missing in JSON request'}), 400
        
        query_text = data['query']
        
        # Perform query processing
        results = process_query(query_text, inverted_index, total_docs)
        
        if not results:
            return jsonify({'message': 'No results found for the query'}), 200
        
        # Format and return results
        formatted_results = [{'document_id': doc_id, 'score': score} for doc_id, score in results]
        return jsonify({'results': formatted_results}), 200
    
    elif request.method == 'GET':
        return jsonify({'message': 'This endpoint only accepts POST requests for querying.'}), 405

if __name__ == '__main__':
    # Load inverted index
    index_filename = "inverted_index.pickle"
    inverted_index = load_inverted_index(index_filename)
    total_docs = len(inverted_index)  # Total number of documents in the inverted index
    
    app.run(debug=True)
