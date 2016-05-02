# InfilectCodingChallenge
Solution for Infilect coding challenge.

Requirements:
==============

1. python 2.7
2. postgres
3. Psycopg2
4. BeautifulSoup
5. SQLAlchemy
6. NLTK (Stopwords / Porter Stemmer)

Steps:
=======

Create database called "jabong"
Edit the DB connection lines in crawl_dress.py, Dress.py to include your database credentials
Run Dress.py to create required table
Run get_links.py to crawl the dresses page to get ~10000 links to dresses
This will create a links file which contains a list of links to crawl
Run crawl_dress to crawl individual dress page to extract the required details and populate in the database
Run the following two commans to mark "party" dresses
  update dress set is_party=1 where description like '%party%';
  update dress set is_party=1 where description like '%parties%';
Run create_model.py to create a binary classifier. is_party will be set to 2 for the rows which the model predicts to be "party" dresses
  - is_party = 0 for non-party dresse
  - is_party = 1 for party dresses set manually
  - is_party = 2 for party dresses predicted by the model

