import pprint
from pymongo import MongoClient

def insert_majors_collection(db):
    majors = [
            {
                "mid": "CSC",
                "Name": "Computer Science",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                },
            {
                "mid": "MATH",
                "Name": "Mathematics",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                }
            ]
    # Inserting multiple documents (rows) into the collection (table)
    # Note: To insert one document, object must be a dictionary and use
    # insert_one(object)
    db.majors_collection.insert_many(majors)

def check_insertion_majors(db):
    # Get all the documents in a collection with find()
    print("\nPRINTING ALL MAJORS")
    for major in db.majors_collection.find():
        pprint.pprint(major)
    # Get first document matching the condition passed in from a collection with
    # find_one(). If nothing is specified, first doc in collection is passed back
    print("\nQUERYING CSC")
    major_obj = db['majors_collection'].find_one({"mid":"CSC"})
    pprint.pprint(major_obj);
    print("\nQUERYING MATH")
    major_obj = db['majors_collection'].find_one({"mid":"MATH"})
    pprint.pprint(major_obj);

def insert_minors_collection(db):
    minors = [
            {
                "mid": "DATA",
                "Name": "Data Science",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                },
            {
                "mid": "MATH",
                "Name": "Mathematics",
                "Needed": [],
                "Support": [],
                "GEs": [],
                "Units": 0,
                "Concentrations": []
                }
            ]
    # Inserting multiple documents (rows) into the collection (table)
    # Note: To insert one document, object must be a dictionary and use
    # insert_one(object)
    db.minors_collection.insert_many(minors)

def check_insertion_minors(db):
    # Get all the documents in a collection with find()
    print("\nPRINTING ALL MINORS")
    for minor in db.minors_collection.find():
        pprint.pprint(minor)
    # Get first document matching the condition passed in from a collection with
    # find_one(). If nothing is specified, first doc in collection is passed back
    print("\nQUERYING DATA")
    major_obj = db['minors_collection'].find_one({"mid":"DATA"})
    pprint.pprint(major_obj);

def insert_classes_collection(db):
    classes = [
            {
                "cid": "CSC_202",
                "Name": "Data Structures",
                "Prereqs": [],
                "Majors": [], #Should be mid
                "Terms_offered": [],
                "Units": 0,
                "USCP": False,
                "GWR": False
                },
            {
                "cid": "MATH_143",
                "Name": "Calculus III",
                "Prereqs": [],
                "Majors": [], #Should be mid
                "Terms_offered": [],
                "Units": 0,
                "USCP": False,
                "GWR": False
                }
            ]
    # Inserting multiple documents (rows) into the collection (table)
    # Note: To insert one document, object must be a dictionary and use
    # insert_one(object)
    db.classes_collection.insert_many(classes)


def check_insertion_classes(db):
    # Get all the documents in a collection with find()
    print("\nPRINTING ALL CLASSES")
    for classs in db.classes_collection.find():
        pprint.pprint(classs)
    # Get first document matching the condition passed in from a collection with
    # find_one(). If nothing is specified, first doc in collection is passed back
    print("\nQUERYING CSC_202")
    major_obj = db['classes_collection'].find_one({"cid":"CSC_202"})
    pprint.pprint(major_obj);
    print("\nQUERYING MATH_143")
    major_obj = db['classes_collection'].find_one({"cid":"MATH_143"})
    pprint.pprint(major_obj);

def insert_general_ed_collection(db):
    general_ed = [
            {
                "gid": "A1",
                "classes": [],
                "majors":[]
                },
            {
                "gid": "A2",
                "classes": [],
                "majors":[]
                }
            ]
    # Inserting multiple documents (rows) into the collection (table)
    # Note: To insert one document, object must be a dictionary and use
    # insert_one(object)
    db.general_ed_collection.insert_many(general_ed)


def check_insertion_general_ed(db):
    # Get all the documents in a collection with find()
    print("\nPRINTING ALL GENERAL ED")
    for ge in db.general_ed_collection.find():
        pprint.pprint(ge)
    # Get first document matching the condition passed in from a collection with
    # find_one(). If nothing is specified, first doc in collection is passed back
    print("\nQUERYING A1")
    major_obj = db['general_ed_collection'].find_one({"gid":"A1"})
    pprint.pprint(major_obj);

client = MongoClient()
dbnames = client.list_database_names()
dbname = "prereq"
if dbname in dbnames:
    print("Dropping database", dbname)
    client.drop_database(dbname)
prereq_db = client[dbname]
insert_majors_collection(prereq_db)
insert_minors_collection(prereq_db)
insert_classes_collection(prereq_db)
insert_general_ed_collection(prereq_db)
# Uncomment below four lines for testing purposes. Caution: very long output. 
check_insertion_majors(prereq_db)
check_insertion_minors(prereq_db)
check_insertion_classes(prereq_db)
check_insertion_general_ed(prereq_db)
print("\nAll Collections:")
pprint.pprint(prereq_db.list_collection_names())
