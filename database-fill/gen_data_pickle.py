"""
This script is used to generate the random data records and store them in pickle files
"""
from essential_generators import DocumentGenerator
from coolname import generate_slug
import names
import random
import pickle
from tqdm import tqdm

# initialize random document generator
gen = DocumentGenerator()

# number of records per table
record_per_table = 1000000

# generate Disaster data
with open('data-pickles/disaster.pkl', 'wb') as f:
    disaster_data = list()
    unique_names = list()
    for id in tqdm(range(record_per_table)):
        while(True):
            name = generate_slug(random.randint(2,4))
            if name not in unique_names:
                unique_names.append(name)
                break
        disaster_data.append([name, gen.sentence(), gen.sentence(), random.randint(1,20)])
    pickle.dump(disaster_data, f)

# generate Incident data
with open('data-pickles/incident.pkl', 'wb') as f:
    incident_data = list()
    for id in tqdm(range(record_per_table)):
        incident_data.append([random.randint(1950,2020), random.randint(1,12), random.randint(1,30), gen.sentence(), 
                            random.randint(1,100000), generate_slug(3), generate_slug(2), random.randint(0,record_per_table-1),
                            random.randint(3*int(record_per_table/4),record_per_table-1)])
    pickle.dump(incident_data, f)

# generate Person data
with open('data-pickles/person.pkl', 'wb') as f:
    person_data = list()
    for id in tqdm(range(record_per_table)):
        person_data.append([names.get_full_name(), random.randint(20,60), random.randint(0,1), generate_slug(3)])
    pickle.dump(person_data, f)

# generate Casualty data
with open('data-pickles/casualty.pkl', 'wb') as f:
    casualty_data = list()
    unique_ids = list(range(0,int(record_per_table/4)-1))
    for id in tqdm(range(int(record_per_table/4))):
        idx = random.choice(unique_ids)
        casualty_data.append([idx, random.randint(1,10)])
        unique_ids.remove(idx)
    pickle.dump(casualty_data, f)

# generate Government_Representative data
with open('data-pickles/govn_rep.pkl', 'wb') as f:
    govn_rep_data = list()
    unique_ids = list(range(int(record_per_table/4),2*int(record_per_table/4)-1))
    for id in tqdm(range(int(record_per_table/4))):
        idx = random.choice(unique_ids)
        govn_rep_data.append([idx, generate_slug(2), generate_slug(3)])
        unique_ids.remove(idx)
    pickle.dump(govn_rep_data, f)

# generate Citizen data
with open('data-pickles/citizen.pkl', 'wb') as f:
    citizen_data = list()
    unique_ids = list(range(2*int(record_per_table/4),3*int(record_per_table/4)-1))
    for id in tqdm(range(int(record_per_table/4))):
        idx = random.choice(unique_ids)
        citizen_data.append([idx, generate_slug(2), generate_slug(3), random.randint(1,10)])
        unique_ids.remove(idx)
    pickle.dump(citizen_data, f)

# generate Criminal data
with open('data-pickles/criminal.pkl', 'wb') as f:
    criminal_data = list()
    unique_ids = list(range(3*int(record_per_table/4),record_per_table-1))
    for id in tqdm(range(int(record_per_table/4))):
        idx = random.choice(unique_ids)
        criminal_data.append([idx, random.randint(1,20)])
        unique_ids.remove(idx)
    pickle.dump(criminal_data, f)

# generate Report data
with open('data-pickles/report.pkl', 'wb') as f:
    report_data = list()
    for id in tqdm(range(record_per_table)):
        report_data.append([gen.sentence(), random.randint(0,record_per_table-1), random.randint(int(record_per_table/4),2*int(record_per_table/4)-1),
                            random.randint(2*int(record_per_table/4),3*int(record_per_table/4)-1)])
    pickle.dump(report_data, f)

# generate Casualty_Incident data
with open('data-pickles/casualty_incident.pkl', 'wb') as f:
    casualty_incident_data = list()
    pairs_list = list()
    for id in tqdm(range(record_per_table)):
        while(True):
            pair = (random.randint(0,record_per_table-1), random.randint(0,int(record_per_table/4)-1))
            if pair not in pairs_list:
                pairs_list.append(pair)
                break
        casualty_incident_data.append([pair[0], pair[1]])
    pickle.dump(casualty_incident_data, f)
