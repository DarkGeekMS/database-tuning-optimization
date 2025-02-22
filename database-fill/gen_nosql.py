import json
import pickle
import datetime
import re

# load data lists
with open('data-pickles/disaster.pkl', 'rb') as f:
    disaster_list = pickle.load(f)
with open('data-pickles/incident.pkl', 'rb') as f:
    incident_list = pickle.load(f)
with open('data-pickles/person.pkl', 'rb') as f:
    person_list = pickle.load(f)
with open('data-pickles/casualty.pkl', 'rb') as f:
    casualty_list = pickle.load(f)
with open('data-pickles/govn_rep.pkl', 'rb') as f:
    govn_rep_list = pickle.load(f)
with open('data-pickles/citizen.pkl', 'rb') as f:
    citizen_list = pickle.load(f)
with open('data-pickles/criminal.pkl', 'rb') as f:
    criminal_list = pickle.load(f)
with open('data-pickles/report.pkl', 'rb') as f:
    report_list = pickle.load(f)
with open('data-pickles/casualty_incident.pkl', 'rb') as f:
    casualty_incident_list = pickle.load(f)

# save reports collection
with open('nosql-collections/reports.json', 'w+') as f:
    for id in range(len(report_list)):
        document = dict()
        document["_id"] = id
        document["content"] = re.sub('[^A-Za-z0-9]+', '', report_list[id][0])
        document["report_date"] = datetime.datetime(2020, 1, 4, 13, 00).strftime("%m/%d/%Y, %H:%M:%S")
        incident_id = report_list[id][1]
        disaster_id = incident_list[incident_id][7]
        casualties_ids = [casualty_incident_pair[1] for casualty_incident_pair in casualty_incident_list if casualty_incident_pair[0] == incident_id]
        document["incident"] = {
            "year" : incident_list[incident_id][0],
            "month" : incident_list[incident_id][1],
            "day" : incident_list[incident_id][2],
            "description" : re.sub('[^A-Za-z0-9]+', '', incident_list[incident_id][3]),
            "eco_loss" : incident_list[incident_id][4],
            "location" : re.sub('[^A-Za-z0-9]+', '', incident_list[incident_id][5]),
            "name" : re.sub('[^A-Za-z0-9]+', '', incident_list[incident_id][6]),
            "type" : {
                "name" : re.sub('[^A-Za-z0-9]+', '', disaster_list[disaster_id][0]),
                "possible_causes" : re.sub('[^A-Za-z0-9]+', '', disaster_list[disaster_id][1]),
                "precaustions" : re.sub('[^A-Za-z0-9]+', '', disaster_list[disaster_id][2]),
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
        document["name"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][0])
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][3])
        document["deg_of_loss"] = casualty_list[id][1]
        json.dump(document, f)
    for id in range(len(govn_rep_list)):
        document = dict()
        document["_id"] = govn_rep_list[id][0]
        document["name"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][0])
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][3])
        document["username"] = re.sub('[^A-Za-z0-9]+', '', govn_rep_list[id][1])
        document["password"] = re.sub('[^A-Za-z0-9]+', '', govn_rep_list[id][2])
        document["data_of_join"] = datetime.datetime(2020, 1, 4, 13, 00).strftime("%m/%d/%Y, %H:%M:%S")
        json.dump(document, f)
    for id in range(len(citizen_list)):
        document = dict()
        document["_id"] = citizen_list[id][0]
        document["name"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][0])
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][3])
        document["username"] = re.sub('[^A-Za-z0-9]+', '', govn_rep_list[id][1])
        document["password"] = re.sub('[^A-Za-z0-9]+', '', govn_rep_list[id][2])
        document["data_of_join"] = datetime.datetime(2020, 1, 4, 13, 00).strftime("%m/%d/%Y, %H:%M:%S")
        document["trust_level"] = citizen_list[id][3]
        json.dump(document, f)
    for id in range(len(criminal_list)):
        document = dict()
        document["_id"] = criminal_list[id][0]
        document["name"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][0])
        document["age"] = person_list[document["_id"]][1]
        document["gender"] = person_list[document["_id"]][2]
        document["address"] = re.sub('[^A-Za-z0-9]+', '', person_list[document["_id"]][3])
        document["no_of_crimes"] = criminal_list[id][1]
        json.dump(document, f)
