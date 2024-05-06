
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
* Computer TF-IDF score/weight representation, Cosine similarity.

#### Processor:
****
* A Flask based Processor for handling free text queries in json format -query processing:
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
        2.Calculates cosine similarity during query execution for efficient search 
        3.Utilizes Scikit-Learn to construct the inverted index and perform efficient searching.

**Processor (Flask-based):** The Processor handles free text queries in JSON format.
* *Query Processing:* 

        1.Validates and error-checks the incoming queries.
        2.Ranks and returns top-K results based on the query.
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

*Flask_App Module:*

        - Handles free text queries in JSON format.
        - Validates and error-checks the incoming queries.
        - Ranks and returns top-K results based on the query.

*Scraper Module*

        Spiders Module
            Manages the crawling by downloading web documents
   
     
#### Interfaces and Implementations:

*Crawler Controller:*

* bookspider.py

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
  pip install Flask
```
Create genspider
```bash
  scrapy genspider BookCrawlerSpider
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
  scrapy crawl bookcrawlerspider
```

Create the Index:
Run the below command in the terminal
```bash
  cd SearchEngine/scraper/spiders
  cd SearchEngine/Flask_app/
  python indexer.py
```

Run the Processor:
Run the below command in the terminal, this will start the Flask server
```bash
  cd SearchEngine/Flask_app/
  python flask_processor.py
```

Client Query the SearchEngine: Run the below command in the terminal
```bash
  cd SearchEngine/Flask_app/
  python query_client.py
```
Client can also query the SearchEngine via  http://127.0.0.1:5000/

