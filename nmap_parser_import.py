import re
from pymongo import MongoClient

def parse_nmap_text_output(nmap_text_output):
    result = []
    current_host = None
    lines = nmap_text_output.splitlines()
    for line in lines:
        if "Nmap scan report for" in line:
            host_line = line.split(" ")
            host_name = host_line[4]
            current_host = {"_id": host_name, "scan": {}}
            result.append(current_host)
        elif "/tcp" in line or "/udp" in line:
            port_line = line.split(" ")
            portid = port_line[0].split("/")
            protocol = portid[1]
            portid = portid[0]
            state = ""
            service = ""
            match = re.search(r"\d+/(tcp|udp)\s+(\w+)\s+(\w+)?", line)
            if match:
                state = match.group(2)
                service = match.group(3) if match.group(3) else ""
            current_host["scan"][portid] = {"Protocol": protocol, "State": state, "Service": service}
    return result

nmap_text_file = ""  # Nmap scan file 

with open(nmap_text_file, "r") as file:
    nmap_text_output = file.read()

parsed_output = parse_nmap_text_output(nmap_text_output)

mongo_host = 'mongodb+srv://cluster0.i3nye.mongodb.net'  # MongoDB host
mongo_port = 27017  # MongoDB port
mongo_db = ''  #  MongoDB database name
mongo_user = ''  # MongoDB username
mongo_password = ''  # MongoDB password

client = MongoClient(host=mongo_host, port=mongo_port, username=mongo_user, password=mongo_password)

db = client[mongo_db]
collection = db["nmap"]  # MongoDB collection name

for doc in parsed_output:
    collection.insert_one(doc)

print(f"Nmap text output has been parsed and imported into MongoDB collection '{collection.name}'.")
