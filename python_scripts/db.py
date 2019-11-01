from pymongo import MongoClient

client = MongoClient()  
db = client['webscraping'] # access db
collection = db['documents'] # access collection