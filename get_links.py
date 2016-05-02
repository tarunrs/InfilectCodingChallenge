from bs4 import BeautifulSoup
import urllib2
import pickle
l = []
for i in range(200):
  html_doc = urllib2.urlopen('http://www.jabong.com/women/clothing/dresses-jumpsuits/dresses/?ax=1&page=' + str(i+1)+'&limit=52&sortField=popularity&sortBy=desc').read()
  doc= BeautifulSoup(html_doc, 'html.parser')
  for link in doc.find_all('a'):
     print (link.get('href'))
     l.append(link.get('href'))
     
pickle.dump(l, open("links", "w"))
