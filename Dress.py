from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text
# Create DB connection - Edit the below line to include your username and password
engine = create_engine('postgresql://tarun:tarun123@localhost:5432/jabong')

#Declare an instance of the Base class for mapping tables
Base = declarative_base()
 
class Dress(Base):
    __tablename__ = 'dress'
    dress_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    brand = Column(String(255))
    image = Column(String(2048))    
    standard_price = Column(String(16))
    actual_price = Column(String(16))
    description = Column(Text)
    type = Column(String(255))
    fabric = Column(String(255))
    sleeves = Column(String(255))
    fit = Column(String(255))
    color = Column(String(255))
    style = Column(String(255))
    length = Column(String(255))
    neck = Column(String(255))    
    sku = Column(String(255))
    is_party = Column(Integer)
    
    def __init__ (self, details):
      self.name = details["title"]
      self.brand = details["brand"]
      self.image = details["image"]      
      self.standard_price = details["standard-price"]
      self.actual_price = details["actual-price"]
      self.description = details["desc"]
      self.type = details["type"]
      self.fabric = details["fabric"]
      self.sleeves = details["sleeves"]
      self.fit = details["fit"]
      self.color = details["color"]
      self.style = details["style"]
      self.length = details["length"]
      self.neck = details["neck"]
      self.sku = details["sku"]
      self.is_party = 0
      
#Create the table using the metadata attribute of the base class
Base.metadata.create_all(engine)

#Close the connection
engine.dispose()


