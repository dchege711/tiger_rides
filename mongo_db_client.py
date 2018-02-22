"""

"""

#_______________________________________________________________________________

import os
from pymongo import MongoClient, IndexModel, TEXT, DESCENDING, HASHED
from pprint import pprint
from bson.son import SON

#_______________________________________________________________________________

class tiger_rides_db():
	
	def __init__(self):
		self.client = MongoClient(os.environ["TIGER_RIDES_MONGO_URI"])
		self.db = self.client["dgitau_orf401"]
		
		self.collection = self.db["attendee_details"]
		
	def _initialize(self):
		self.collection.drop_indexes()
		self.collection.create_index([("email", TEXT)], unique=True)
		self.collection.create_index([("first_name", DESCENDING)])
		self.collection.create_index([("last_name", DESCENDING)])
		self.collection.create_index([("origin", HASHED)])
		self.collection.create_index([("leaving_date", DESCENDING)])
		self.collection.create_index([("leaving_time", DESCENDING)])
		self.collection.create_index([("has_car", DESCENDING)])
		self.collection.create_index([("password", DESCENDING)])
		
	def create(self, doc):
		return self.collection.insert_one(doc)
	
	def update(self, filter_key, key_value_pairs):
		return self.collection.update_one(
			filter_key,
			{"$set": key_value_pairs}
		)
		
	def read(self, query):
		return self.collection.find_one(filter=query)
		
def main():
	tiger_rides = tiger_rides_db()
	# tiger_rides._initialize()
	# tiger_rides.create({
	# 	"email": "nothing@gmail.com",
	# 	"first_name": "Kaboom",
	# 	"last_name": "Psyche",
	# 	"origin": "Nashville",
	# 	"leaving_date": "01-01-2018",
	# 	"leaving_time": "12:34PM",
	# 	"has_car": "no",
	# 	"password": "lets_save_passwords_in_plain_text"
	# })
	print(tiger_rides.read({"origin": "Nashville"}))
	
	
	

if __name__ == "__main__":
	main()
