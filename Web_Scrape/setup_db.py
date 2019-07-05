import pprint
from pymongo import MongoClient
client = MongoClient()
dbnames = client.list_database_names()
dbname = "prereq"
if dbname in dbnames:
    print("Dropping database")
    client.drop_database(dbname)
prereq_db = client[dbname]
majors = {
        "CSC": {
                "Name": "Computer Science",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                },
         "MATH": {
                "Name": "Mathematics",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                }
        }
collection = prereq_db.majors_collection
doc_id = collection.insert_one(majors).inserted_id
pprint.pprint(doc_id)
pprint.pprint(prereq_db.list_collection_names())
pprint.pprint(collection.find_one())
pprint.pprint(major_obj);
