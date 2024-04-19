import requests

def send_query(query_text):
    # Define the URL of the Flask server
    url = "http://127.0.0.1:5000/query"
    
    # Prepare the payload containing the query text
    payload = {"query": query_text}
    
    # Send a POST request to the server
    response = requests.post(url, json=payload)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        
        # Extract and return the search results
        results = json_response.get("results")
        return results
    else:
        # If the request was not successful, print an error message
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    query = "hyperbole and a half"
    results = send_query(query)
    
    if results:
        print("Search Results:")
        for result in results:
            #print(result)
            print(f"Document ID: {result['document_id']}, Title: {result['title']}, Score: {result['score']}")
    else:
        print("No results found.")

