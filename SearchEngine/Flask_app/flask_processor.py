from flask import Flask, request, jsonify, render_template
import re
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
    text = text.lower()  # Convert to lowercase
    # Tokenize multi-word phrases and single words
    tokens = re.findall(r'\b\w+(?:-\w+)*\b|\b\w+\b', text)
    tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    return ' '.join(tokens)

# Function to perform query processing
def process_query(query, inverted_index, total_docs, k=5):
    q = query
    print("query ",q)
    query = preprocess_text(query)
    
    query_terms = query.split()
    print("query_terms ",query_terms)
    
    # Calculate TF-IDF scores for query terms
    query_tfidf = defaultdict(float)
    for term in query_terms:
        if term in inverted_index:
            df = len(inverted_index[term])  # Document frequency (DF)
            idf = math.log10(total_docs / df) if df != 0 else 0  # Inverse Document Frequency (IDF)
            tfidf_query_term = (query_terms.count(term) / len(query_terms)) * idf  # TF-IDF for query term
            query_tfidf[term] = tfidf_query_term
    
    #Rank documents based on cosine similarity with query
    ranked_results = defaultdict(float)
    for term, tfidf_query_term in query_tfidf.items():
        for doc_info in inverted_index[term]:
            doc_id, doc_title, price, availability, tfidf_doc_value = doc_info  # Extract document ID, title, and TF-IDF value
            ranked_results[doc_id] += tfidf_query_term * tfidf_doc_value

    # Sort and get top-K results
    top_results = sorted(ranked_results.items(), key=lambda x: x[1], reverse=True)[:k]

    # Include document titles in the results
    results_with_titles = []
    for doc_id, score in top_results:
        doc_title = ''  # Initialize doc_title
        price = ''
        availability = ''

        # Iterate over all terms to find the postings for the given doc_id
        for term, postings in inverted_index.items():
            for posting in postings:
                if posting[0] == doc_id:  # Check if the doc_id matches
                    doc_title = posting[1]
                    price = posting[2]
                    availability = posting[3]  # Extract doc_title from the posting
                    break  # Stop searching once found
            if doc_title:  # If doc_title is found, break the outer loop
                break
        # Append the result with document ID, title, and score
        results_with_titles.append({'document_id': doc_id, 'title': doc_title, 'price': price, 'availability': availability, 'cosine_score': score})
        print("results_with_titles ", results_with_titles)

    return results_with_titles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    global inverted_index, total_docs  # Access global variables
    
    if request.method == 'POST':
        data = request.get_json()
        print("data ",data)
        if 'query' not in data:
            return jsonify({'error': 'Query field is missing in JSON request'}), 400
       
        query_text = data['query']
        print("query_text ",query_text)
        
        # Perform query processing
        results = process_query(query_text, inverted_index, total_docs)
        
        if not results:
            return jsonify({'message': 'No results found for the query'}), 200
        
        # Format and return results
        formatted_results = [{'document_id': result['document_id'], 'title': result['title'], 'price': result['price'], 'availability': result['availability'], 'cosine_score': result['cosine_score']} for result in results]

        return jsonify({'results': formatted_results}), 200
    
    elif request.method == 'GET':
        return jsonify({'message': 'This endpoint only accepts POST requests for querying.'}), 405



if __name__ == '__main__':
    # Load inverted index
    index_filename = "../scraper/inverted_index.pickle"
    inverted_index = load_inverted_index(index_filename)
    total_docs = len(inverted_index)  # Total number of documents in the inverted index
    
    app.run(debug=True)
