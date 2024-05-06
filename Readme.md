
## BookCrawlerX

### Abstract

The project aims to build a comprehensive web content search engine using Python. It consists of three main components: a Scrapy-based Crawler, a Scikit-Learn-based Indexer, and a Flask-based Processor. 
### Development Summary/Objectives

#### Crawler:
***
* A Scrapy based Crawler for downloading web documents in html format - content crawling:
*  Initialize using seed URL/Domain, Max Pages, Max Depth

#### Indexer:
***
* A Scikit-Learn based Indexer for contructing an inverted index in pickle format - search indexing:
* Computer TF-IDF score/weight representation

#### Processor:
****
* A Flask based Processor for handling free text queries in json format -query processing:
* Cosine similarity is calculated during query processing
* Implement Query validation/error-checking, Top-K ranked results
### Overview

The project is designed to create a comprehensive web document retrieval system.

#### Solution Outline:
***
*  **Crawler(Scrapy-based):** The Crawler is responsible for downloading web documents in HTML format. It initializes using a seed URL/Domain, Max Pages, and Max Depth.
* *Content Crawling*:

        1.Initializes with a seed URL/Domain to start the crawling process.
        2.Limits the number of pages to download with Max Pages.
        3.Limits the depth of crawling with Max Depth.
        4.Utilizes Scrapy to efficiently crawl web pages and extract HTML content.

* **Indexer(Scikit-Learn-based):** The Indexer is responsible for constructing an inverted index in pickle format.
* *Search Indexing*:

        1.Stores the inverted index in pickle format for fast retrieval.
        2.Represents documents using TF-IDF scores/weights.
        3.Utilizes Scikit-Learn to construct the inverted index and perform efficient searching.

**Processor (Flask-based):** The Processor handles free text queries in JSON format.
* *Query Processing:* 

        1.Validates and error-checks the incoming queries.
        2.Ranks based on cosine similarity and returns top-K results based on the query.
        3.Utilizes Flask to handle HTTP requests and responses.
        4.Integrates the Indexer to search and retrieve relevant documents.
        5.Provides results in JSON format for easy consumption by client applications.

#### Relevant Literature:
***
* *Web Crawling and Content Extraction:* The project employs Scrapy, a powerful web crawling framework, to extract content from web documents. Literature such as "Scrapy: An Open Source Web Crawling Framework for Python" by Pablo Hoffman that provides insights into how Scrapy efficiently extracts data from websites.
* *Inverted Index and Information Retrieval:* For the construction of the inverted index and efficient search, the project utilizes Scikit-Learn. Literature such as "Introduction to Information Retrieval" by Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze is a fundamental resource providing a comprehensive understanding of inverted indexes, TF-IDF, and cosine similarity.
* *Query Processing and Flask:* Flask, a micro web framework, is used for processing free text queries. Literature such as "Introduction to Web development using Flask from GeeksForGeeks.org that offers detailed insights into building web applications with Flask.

#### Proposed System:
***
The system aims to provide a robust and efficient web document retrieval system. By combining the power of Scrapy for web crawling, Scikit-Learn for constructing the inverted index, and Flask for query processing, the system will offer high-quality search results. Utilizing TF-IDF score/weight representation, and cosine similarity the system ensures accurate and fast retrieval of relevant documents. With proper query validation and error-checking, along with returning top-K ranked results, the system ensures an intuitive and user-friendly experience.
### Design

#### Interactions:

*Crawler to Indexer:*
* After downloading web documents, the Crawler sends the extracted content to the Indexer.
* The Indexer constructs an inverted index using the TF-IDF scores/weights of the extracted content.

*Indexer to Processor:*
* The Processor sends queries to the Indexer for document retrieval.
* The Indexer searches the inverted index for relevant documents based on the query and returns the results to the Processor.

Integration:

*Crawler and Indexer Integration:*

* The Crawler and Indexer are integrated through a pipeline.
* After the Crawler downloads the web documents, it sends the extracted content to the Indexer.
* The Indexer then constructs the inverted index.

*Indexer and Processor Integration:*

* The Indexer and Processor are integrated to provide efficient search functionality.
* The Processor sends queries to the Indexer, which searches the inverted index for relevant documents based on the query and returns the results to the Processor.

### Architecture

#### Software Components:

*Flask Processor:*

        - Handles free text queries in JSON format.
        - Validates and error-checks the incoming queries.
        - Ranks and returns top-K results based on the query.

*bookcrawlerX - Scraper*

        Spiders Module
        - Handles the crawling process by fetching web documents in HTML format
   
     
#### Interfaces and Implementations:

*Crawler Controller:*

* BookCrawlerSpider.py

        - Contains the information regarding url to be crawled along with max_pages and max_depth
        - States the rules for extracting information from links of the url
        - Downloads ans save the web documents in html format
*Index Controller:*

* indexer.py

        - PreProcess the Text by tokenizing 
        - Creates the inverted index in pickle format by extracting title, price and availability
        - Calculate TF-IDF values

*Processor Controller:*

* flask_processor.py
        
        - Contains the Flask application setup and routes.
        - Processes the validated queries and calculates the cosine similarity and interacts with the  indexer to retrieve relevant documents.

* query_client.py
        
        - Sends queries to the Processor for document retrieval.


### Operation

#### Software Commands and Installation

Create Project
```bash
  scrapy startproject bookcrawlerX
```
![projectCreation](/assets/projectCreation.png)

```bash
  pip install Flask
```

Create genspider
```bash
  scrapy genspider BookCrawlerSpider http://books.toscrape.com/
```    
Install dependencies with pip

```bash
  pip install scrapy
  pip install Flask
```

#### Input

Starting the BookCrawler:
Run the crawler using the following command in the terminal
```bash
  cd SearchEngine/scraper/spiders
  scrapy crawl BookCrawlerSpider
```

Create the Index:
Run the below command in the terminal
```bash
  cd SearchEngine/Indexer
  python indexer.py
```

Run the Processor:
Run the below command in the terminal, this will start the Flask server
```bash
  cd SearchEngine/Flask_Processor/
  python flask_processor.py
```

Client Query the SearchEngine: Run the below command in the terminal
```bash
  cd SearchEngine/Flask_app/
  python query_client.py
```
Client can also query the SearchEngine via  http://127.0.0.1:5000/


### Conclusion

#### Results

###### *Web Crawling*
***
After starting the crawler, we can see status like below:

![scrapySpider](/assets/crawlingStatus.png)

###### *Inverted Index with TF-IDF Value*
***
Inverted Index creation status:

![scrapySpider](/assets/invertedIndex.png)

###### *Flask Processor*
***
Status of Flask Server status along with ranking documents based on cosine similarity with query. Produces TOP-K results:

![scrapySpider](/assets/flaskProcessor.png)

###### *Client*
Produces the top-k results. Here k = 5 

![scrapySpider](/assets/clientQuery.png)
### Data Sources - Links, downloads, access information

- [Books to Scrape](http://books.toscrape.com/)
- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- [Python Documentation](https://docs.python.org/3.11/)

### Test cases

*Test Case for checking inverted index*
***
```python
import pickle

# Function to load the inverted index from pickle file
def load_index_from_pickle(filename):
    with open(filename, 'rb') as f:
        inverted_index = pickle.load(f)
    return inverted_index

# Load the inverted index from pickle file
inverted_index = load_index_from_pickle("../Indexer/inverted_index.pickle")

count = 0
for term, postings in inverted_index.items():
    print(f"Term: {term}")
    print("Postings:")
    for posting in postings:
        print(posting)
    print()
    count += 1
    if count == 10:
        break
```
*Test Case for Querying  the SearchEngine*
***
```python
if __name__ == "__main__":
    # Example usage
    query = "hyperbole and a half" # change this to different query for verification
    results = send_query(query)
    
    if results:
        print("Search Results:")
        for result in results:
            print(result)
    else:
        print("No results found.")
```
### SourceCode

#### Listings

- [BookCrawlerSpider.py](./bookcrawlerX/bookcrawlerX/spiders/BookCrawlerSpider.py)
- [HTML Files Directory](./bookcrawlerX/html_files/)
- [indexer.py](./Indexer/indexer.py)
- [flask_processor.py](./Flask_Processor/flask_processor.py)
- [query_client.py](./Flask_Processor/query_client.py)
- [index.html](./Flask_Processor/templates/index.html)

#### Documentation

- [Flask](https://flask.palletsprojects.com/en/latest/)
- [Requests](https://flask.palletsprojects.com/en/3.0.x/reqcontext/)
- [NLTK-CORPUS](https://www.nltk.org/api/nltk.corpus.html)
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [python collections](https://docs.python.org/3/library/collections.html)
- [python pickle](https://docs.python.org/3/library/pickle.html)

#### Dependencies(Open-Source)

Flask
```bash
pip install Flask
```
Requests
```bash

pip install requests
```

NLTK-Corpus
```bash
pip install nltk
```

Beautiful Soup
```bash
pip install beautifulsoup4
```

scikit-learn
```bash
pip install scikit-learn>=1.2
```
Scrapy
```bash
pip install scrapy
```


### Bibliography

1. Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schütze. *An Introduction to Information Retrieval*. April 2009. http://www.informationretrieval.org/.

2. Wagle, Manil. *Web Scraping Using Scrapy: A Step by Step Guide to Scrape Websites Using Scrapy*. April 10, 2020. https://medium.com/@manilwagle/web-scraping-using-scrapy-ac376100ffb3.

 