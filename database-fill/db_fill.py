"""
This script is used to generate the random data records
"""
from coolname import generate_slug
import random

# number of records per table
record_per_table = 200000

# autofill Disaster table
with open('disaster_fill.sql', 'w+') as f:
    unique_names = list()
    for id in range(record_per_table):
        while(True):
            name = generate_slug(2)
            if name not in unique_names:
                unique_names.append(name)
                break
        f.write(f"INSERT INTO Disaster (name, possible_causes, precautions, no_of_prev_occur) VALUES ('{name}', 'list of possible causes', 'list of precautions', {random.randint(1,20)});\n")

# autofill Incident table
with open('incident_fill.sql', 'w+') as f:
    for id in range(record_per_table):
        f.write(f"INSERT INTO Incident (year, month, day, description, eco_loss, location, name, type, suspect) \
        VALUES ({random.randint(1950,2020)}, {random.randint(1,12)}, {random.randint(1,30)}, 'what happened there?', {random.randint(1,100000)}, \
            'what country?', '{generate_slug(2)}', {random.randint(0,record_per_table-1)}, {random.randint(3*int(record_per_table/4),record_per_table-1)});\n")

# autofill Person table
with open('person_fill.sql', 'w+') as f:
    for id in range(record_per_table):
        f.write(f"INSERT INTO Person (name, age, gender, address) VALUES ('{generate_slug(2)}', {random.randint(20,60)}, {random.randint(0,1)}, 'where you live?');\n")

# autofill Casualty table
with open('casualty_fill.sql', 'w+') as f:
    unique_ids = list()
    for id in range(int(record_per_table/4)):
        while(True):
            idx = random.randint(0,int(record_per_table/4)-1)
            if idx not in unique_ids:
                unique_ids.append(idx)
                break
        f.write(f"INSERT INTO Casualty (id, deg_of_loss) VALUES ({idx}, {random.randint(1,10)});\n")

# autofill Government_Representative table
with open('govn_fill.sql', 'w+') as f:
    unique_ids = list()
    for id in range(int(record_per_table/4)):
        while(True):
            idx = random.randint(int(record_per_table/4),2*int(record_per_table/4)-1)
            if idx not in unique_ids:
                unique_ids.append(idx)
                break
        f.write(f"INSERT INTO Government_Representative (id, username, password) VALUES ({idx}, '{generate_slug(2)}', '{generate_slug(3)}');\n")

# autofill Citizen table
with open('citizen_fill.sql', 'w+') as f:
    unique_ids = list()
    for id in range(int(record_per_table/4)):
        while(True):
            idx = random.randint(2*int(record_per_table/4),3*int(record_per_table/4)-1)
            if idx not in unique_ids:
                unique_ids.append(idx)
                break
        f.write(f"INSERT INTO Citizen (id, username, password, trust_level) VALUES ({idx}, '{generate_slug(2)}', '{generate_slug(3)}', {random.randint(1,10)});\n")

# autofill Criminal table
with open('criminal_fill.sql', 'w+') as f:
    unique_ids = list()
    for id in range(int(record_per_table/4)):
        while(True):
            idx = random.randint(3*int(record_per_table/4),record_per_table-1)
            if idx not in unique_ids:
                unique_ids.append(idx)
                break
        f.write(f"INSERT INTO Criminal (id, no_of_crimes) VALUES ({idx}, {random.randint(1,20)});\n")

# autofill Report table
with open('report_fill.sql', 'w+') as f:
    for id in range(record_per_table):
        f.write(f"INSERT INTO Report (content, incident_id, govn_id, citizen_id) VALUES ('report content', \
            {random.randint(0,record_per_table-1)}, {random.randint(int(record_per_table/4),2*int(record_per_table/4)-1)}, {random.randint(2*int(record_per_table/4),3*int(record_per_table/4)-1)});\n")

# autofill Casualty_Incident table
with open('casualty_incident_fill.sql', 'w+') as f:
    pairs_list = list()
    for id in range(record_per_table):
        while(True):
            pair = (random.randint(0,record_per_table-1), random.randint(0,int(record_per_table/4)-1))
            if pair not in pairs_list:
                pairs_list.append(pair)
                break
        f.write(f"INSERT INTO Casualty_Incident (incident_id, casualty_id) VALUES ({pair[0]}, {pair[1]});\n")
