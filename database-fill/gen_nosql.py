import json
import pickle
import datetime

# load data lists
with open('disaster.pkl', 'rb') as f:
    disaster_list = pickle.load(f)
with open('incident.pkl', 'rb') as f:
    incident_list = pickle.load(f)
with open('person.pkl', 'rb') as f:
    person_list = pickle.load(f)
with open('casualty.pkl', 'rb') as f:
    casualty_list = pickle.load(f)
with open('govn_rep.pkl', 'rb') as f:
    govn_rep_list = pickle.load(f)
with open('citizen.pkl', 'rb') as f:
    citizen_list = pickle.load(f)
with open('criminal.pkl', 'rb') as f:
    criminal_list = pickle.load(f)
with open('report.pkl', 'rb') as f:
    report_list = pickle.load(f)
with open('casualty_incident.pkl', 'rb') as f:
    casualty_incident_list = pickle.load(f)

# save reports collection
with open('nosql-collections/reports.json', 'w+') as f:
    for id in range(len(report_list)):
        document = dict()
        document["_id"] = id
        document["content"] = report_list[id][0]
        document["report_date"] = datetime.datetime(2020, 1, 4, 13, 00)
        incident_id = report_list[id][1]
        disaster_id = incident_list[incident_id][7]
        casualties_ids = [casualty_incident_pair[1] for casualty_incident_pair in casualty_incident_list if casualty_incident_pair[0] == incident_id]
        document["incident"] = {
            "date" : f"{incident_list[incident_id][0]}-{incident_list[incident_id][1]}-{incident_list[incident_id][2]}",
            "description" : incident_list[incident_id][3],
            "eco_loss" : incident_list[incident_id][4],
            "location" : incident_list[incident_id][5],
            "name" : incident_list[incident_id][6],
            "type" : {
                "name" : disaster_list[disaster_id][0],
                "possible_causes" : disaster_list[disaster_id][1],
                "precaustions" : disaster_list[disaster_id][2],
                "no_of_prev_occur" : disaster_list[disaster_id][3]
            },
            "suspect_id" : incident_list[incident_id][8],
            "casualties" : casualties_ids
        }
        document["govn_rep_id"] = report_list[id][2]
        document["citizen_id"] = report_list[id][3]
        json.dump(document, f)

# save persons collection
with open('nosql-collections/persons.json', 'w+') as f:
    for id in range(len(casualty_list)):
        document = dict()
        document["_id"] = casualty_list[id][0]
        document["name"] = person_list[document["_id"]][0]
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = person_list[document["_id"]][3]
        document["deg_of_loss"] = casualty_list[id][1]
        json.dump(document, f)
    for id in range(len(govn_rep_list)):
        document = dict()
        document["_id"] = govn_rep_list[id][0]
        document["name"] = person_list[document["_id"]][0]
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = person_list[document["_id"]][3]
        document["username"] = govn_rep_list[id][1]
        document["password"] = govn_rep_list[id][2]
        document["data_of_join"] = datetime.datetime(2020, 1, 4, 13, 00)
        json.dump(document, f)
    for id in range(len(citizen_list)):
        document = dict()
        document["_id"] = citizen_list[id][0]
        document["name"] = person_list[document["_id"]][0]
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = person_list[document["_id"]][3]
        document["username"] = citizen_list[id][1]
        document["password"] = citizen_list[id][2]
        document["data_of_join"] = datetime.datetime(2020, 1, 4, 13, 00)
        document["trust_level"] = citizen_list[id][3]
        json.dump(document, f)
    for id in range(len(criminal_list)):
        document = dict()
        document["_id"] = criminal_list[id][0]
        document["name"] = person_list[document["_id"]][0]
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = person_list[document["_id"]][3]
        document["no_of_crimes"] = criminal_list[id][1]
        json.dump(document, f)
