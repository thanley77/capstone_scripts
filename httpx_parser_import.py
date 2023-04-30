import pymongo
import json
from pymongo import MongoClient
from json import JSONDecodeError
## only works for 1 single host
def import_to_mongodb(json_file, mongo_db, collection):

    mongo_host = 'mongodb+srv://cluster17882.hwp8jti.mongodb.net'  #MongoDB host
    mongo_port = 27017  # MongoDB port
    mongo_db = ''  # MongoDB database name
    mongo_user = ''  # MongoDB username
    mongo_password = ''  #  MongoDB password

    client = MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_password)

    db = client[mongo_db]
    collection = db[""] #collection name, can be a new one or existing one
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
            collection.insert_one(data)
        except JSONDecodeError as e:
            print(f"Error decoding JSON from file '{json_file}': {e}")
            f.seek(0)
            try:
                formatted_data = json.load(f)
                with open(json_file, 'w') as f:
                    json.dump(formatted_data, f, indent=4)
                print(f"Successfully formatted JSON file: '{json_file}'")
            except Exception as e:
                print(f"Error formatting JSON file '{json_file}': {e}")
                 
import_to_mongodb('httpx.json.out', 'pentests_hyatt', 'httpx') #input file, database name, collection name
