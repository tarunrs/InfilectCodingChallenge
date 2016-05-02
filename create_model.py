from sqlalchemy import create_engine, desc,update
from sqlalchemy.orm import sessionmaker
from Dress import Dress
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import cross_validation

engine = create_engine('postgresql://tarun:tarun123@localhost:5432/jabong')
Session = sessionmaker(bind=engine)
session= Session()

stops = set(stopwords.words("english"))
#stops.add("party")
stemmer = PorterStemmer()

def dress_to_words(dress):
  dress_text = " ".join(
                     [dress.description, dress.name, dress.brand, 
                     dress.type, dress.fabric, dress.sleeves, dress.fit, 
                     dress.color, dress.style, dress.length, dress.neck])
  # Remove punctuation etc.
  letters_only = re.sub("[^a-zA-Z]", " ", dress_text) 
  #
  # Convert to lower case, split into individual words
  words = letters_only.lower().split()                             
  # 
  # Remove stop words
  meaningful_words = [w for w in words if not w in stops]   
  #
  # Stem the words
  feature_words = [stemmer.stem(w)  for w in meaningful_words ]   
  return( " ".join(feature_words))   

dress_ids = []
dress_words = []
dress_classes = []

for dress in session.query(Dress).order_by(desc(Dress.is_party)).all():
  dress_ids.append(dress.dress_id)
  dress_words.append(dress_to_words(dress))
  dress_classes.append(dress.is_party)
  
# Create bag of words feature vectors
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)  
features = vectorizer.fit_transform(dress_words)
features = features.toarray()

# First 2031 elements of features are party dresses
train_data_features = features [0:3000]
test_data_features = features [3000:]

#Validate model using 60/40 training/testing split
forest = RandomForestClassifier(n_estimators = 100) 
X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_data_features, dress_classes[0:3000], test_size=0.4, random_state=1)
forest = forest.fit( X_train, y_train )
print "Score:", forest.score(X_test, y_test)

#Train on all sample to generate final model
forest = RandomForestClassifier(n_estimators = 100) 
forest = forest.fit( train_data_features, dress_classes[0:3000] )
result = forest.predict(test_data_features)

count = 0
for i in range(len(result)):
  if result[i] == 1:
    count = count + 1
    session.query(Dress).filter(Dress.dress_id == dress_ids[3000+i]).update({"is_party": 2})
    session.commit()
print "# marked as party: ", count
engine.dispose()
