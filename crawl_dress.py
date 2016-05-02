import urllib2
from bs4 import BeautifulSoup
import json 
import pickle
from time import time, strftime, localtime
from collections import defaultdict
import unicodedata
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Dress import Dress

def get_product_details(doc, link):
  product_details = defaultdict(str)
  try:
   unicode_str = doc.find("span", {"class": "brand"}).getText()
   product_details["brand"] = unicodedata.normalize('NFKD',unicode_str).encode('ascii', 'ignore')
   unicode_str = doc.find("span", {"class": "product-title"}).getText()
   product_details["title"] = unicodedata.normalize('NFKD',unicode_str).encode('ascii', 'ignore')
   unicode_str = doc.find("h2",{"class":"prod-disc"}).getText()
   product_details["desc"] =  unicodedata.normalize('NFKD',unicode_str).encode('ascii', 'ignore')
   if doc.find("span", {"class": "standard-price"}) != None:
     unicode_str = doc.find("span", {"class": "standard-price"}).getText()
     product_details["standard-price"] = unicodedata.normalize('NFKD',unicode_str).encode('ascii', 'ignore')
   unicode_str = doc.find("span", {"class": "actual-price"}).getText()
   product_details["actual-price"] = unicodedata.normalize('NFKD',unicode_str).encode('ascii', 'ignore')
   img_config = doc.find("img",{"class":"primary-image"}).get("data-img-config") 
   product_details["image"] =  str(json.loads(img_config)['base_path'] + ".jpg")

   lis = doc.find("ul",{"class":"prod-main-wrapper"}).findAll("li")  

   for li in lis:
     label = str(li.find("label").getText()).lower()
     value = str(li.find("span").getText()) 
     product_details[label] = value
  except: 
    print "Parse Error: ", link
  
  return product_details

#Setup database connections
engine = create_engine('postgresql://tarun:tarun123@localhost:5432/jabong')
Session = sessionmaker(bind=engine)
session = Session()

#Load links to be crawled/scrapped
links = pickle.load(open("links", "r"))

i = 0
for link in links:
  i = i + 1
  html_link = 'http://www.jabong.com' + link
  print i 
  try :
    html_doc = urllib2.urlopen(html_link)
    doc = BeautifulSoup(html_doc, 'html.parser')
    pd = get_product_details(doc, html_link)
    dress = Dress(pd)
    session.add(dress)
    try:
      session.commit()
    except SQLAlchemyError as e:
      print (str(e)) 
  except:
    print "ERROR: ", html_link
  



