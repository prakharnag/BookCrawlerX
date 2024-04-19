import os
import math
from bs4 import BeautifulSoup
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict, Counter

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Function to preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]  # Remove stop words
    return ' '.join(tokens)

# Function to build inverted index from HTML files
def build_inverted_index(html_files_dir):
    print("Building inverted index...")
    inverted_index = defaultdict(list)
    total_docs = len(os.listdir(html_files_dir))
    all_terms_list = []
    all_unique_terms_dict = {}
    df_counts = Counter()  # Initialize df_counts
    
    # Iterate over HTML files
    for doc_index, filename in enumerate(os.listdir(html_files_dir)):
        print(f"Processing file: {filename}")
        with open(os.path.join(html_files_dir, filename), 'r', encoding='utf-8') as f:
            html_content = f.read()
            # Extract textual data from HTML (e.g., title, price, availability)
            # For demonstration purposes, let's assume we're extracting the title only
            title = extract_title(html_content)
            # Preprocess text
            preprocessed_title = preprocess_text(title)
            # Skip documents with empty preprocessed text
            if not preprocessed_title:
                print(f"Skipping document {filename} due to empty preprocessed text.")
                continue
            # Update inverted index with unique terms and TF-IDF values
            terms = preprocessed_title.split()  # Split into terms
            unique_terms = set(terms)  # Consider only unique terms
            all_unique_terms_dict[f"\nDocument {doc_index + 1}"] = unique_terms  # Store unique terms for the current document
            for term in unique_terms:
                df_counts[term.lower()] += 1  # Update df_counts
                tf_idf = tfidf_value(term, terms, total_docs, df_counts)
                inverted_index[term].append((doc_index + 1, tf_idf))
                all_terms_list.append(terms)  # Store terms for all documents

    if not all_terms_list:
        print("No documents with non-empty preprocessed text found. Aborting.")
        return None

    print("Inverted index successfully built.")
    return inverted_index

def tfidf_value(term, terms, total_docs, df_counts):
    tf = terms.count(term) / len(terms)  # TF (Term Frequency)
    df = df_counts[term]  # DF (Document Frequency)
    idf = math.log10(total_docs / df) if df != 0 else 0  # IDF (Inverse Document Frequency)
    return tf * idf

# Function to save inverted index to a file
def save_inverted_index(inverted_index, index_filename):
    print(f"Saving inverted index to file: {index_filename}")
    with open(index_filename, 'wb') as f:
        pickle.dump(inverted_index, f)
    print("Inverted index saved successfully.")

# Function to extract title from HTML content
def extract_title(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the <title> tag and extract its text
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text(strip=True)
    else:
        return ""

# Example usage:
html_files_dir = "indeedscraper/spiders/html_files"
index_filename = "inverted_index.pickle"

inverted_index = build_inverted_index(html_files_dir)
if inverted_index is not None:
    save_inverted_index(inverted_index, index_filename)
    
    # Print top 10 values of inverted index with TF-IDF scores
    print("\nInverted Index with TF-IDF scores:")
    for term, postings in list(inverted_index.items())[:10]:
        print(f"\n{term} -> {postings}")
