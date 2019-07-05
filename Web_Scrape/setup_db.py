import pprint
from pymongo import MongoClient
client = MongoClient()
dbnames = client.list_database_names()
dbname = "prereq"
if dbname in dbnames:
    print("Dropping database")
    client.drop_database(dbname)
prereq_db = client[dbname]
majors = [
        {
            "cid": "CSC",
            "Name": "Computer Science",
            "Needed": [],
            "Support": [],
            "GEs": [],
            "Units": 0,
            "Concentrations": []
            },
        {
            "cid": "MATH",
            "Name": "Mathematics",
            "Needed": [],
            "Support": [],
            "GEs": [],
            "Units": 0,
            "Concentrations": []
            }
         ]
# Getting a collection (table) from a database
collection = prereq_db.majors_collection
# Inserting multiple documents (rows) into the collection (table)
# Note: To insert one document, object must be a dictionary and use
# insert_one(object)
collection.insert_many(majors)
pprint.pprint(prereq_db.list_collection_names())
# Get all the documents in a collection with find()
print("\nPRINTING ALL MAJORS")
for major in collection.find():
    pprint.pprint(major)
# Get first document matching the condition passed in from a collection with
# find_one(). If nothing is specified, first doc in collection is passed back
print("\nQUERYING CSC")
major_obj = prereq_db['majors_collection'].find_one({"cid":"CSC"})
pprint.pprint(major_obj);
print("\nQUERYING MATH")
major_obj = prereq_db['majors_collection'].find_one({"cid":"MATH"})
pprint.pprint(major_obj);

