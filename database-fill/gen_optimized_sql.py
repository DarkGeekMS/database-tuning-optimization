"""
This script is used to convert data pickles into sql queries (for optimized schema)
"""
import pickle
import sys

# number of records per table
record_per_table = int(sys.argv[1])

# read person table
with open('data-pickles/person.pkl', 'rb') as f:
    persons_list = pickle.load(f)
persons_offset = int(len(persons_list)/4)

# autofill Disaster table
with open('data-pickles/disaster.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/causes_fill.sql', 'w+') as f:
    query = "INSERT INTO Causes \n(corpus) \nVALUES\n"
    for id in range(record_per_table):
        text = data_list[id][1].replace("'", "")
        if id == 0:
            query += f"('{text}')"
            continue
        query += f",\n('{text}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/precautions_fill.sql', 'w+') as f:
    query = "INSERT INTO Precautions \n(corpus) \nVALUES\n"
    for id in range(record_per_table):
        text = data_list[id][2].replace("'", "")
        if id == 0:
            query += f"('{text}')"
            continue
        query += f",\n('{text}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/disaster_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Disaster \n(name, possible_causes, precautions, no_of_prev_occur) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"('{data_list[id+sub_id][0][:40]}', {id}, {id}, {data_list[id+sub_id][3]});\n"
            else:
                query += f"('{data_list[id+sub_id][0][:40]}', {id}, {id}, {data_list[id+sub_id][3]}),\n"
        f.write(query)
            
# autofill Incident table
with open('data-pickles/incident.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/descriptions_fill.sql', 'w+') as f:
    query = "INSERT INTO Descriptions \n(corpus) \nVALUES\n"
    for id in range(record_per_table):
        text = data_list[id][3].replace("'", "")
        if id == 0:
            query += f"('{text}')"
            continue
        query += f",\n('{text}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/incident_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Incident (inc_date, description, eco_loss, location, name, type, suspect) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"('{data_list[id+sub_id][0]}-{str(data_list[id+sub_id][1]).zfill(2)}-{str(max(1,data_list[id+sub_id][2]-2)).zfill(2)}', \
                        {id}, {data_list[id+sub_id][4]}, '{data_list[id+sub_id][5][:60]}', \
                        '{data_list[id+sub_id][6][:40]}', {data_list[id+sub_id][7]}, {data_list[id+sub_id][8]-3*persons_offset});\n"
            else:
                query += f"('{data_list[id+sub_id][0]}-{str(data_list[id+sub_id][1]).zfill(2)}-{str(max(1,data_list[id+sub_id][2]-2)).zfill(2)}', \
                        {id}, {data_list[id+sub_id][4]}, '{data_list[id+sub_id][5][:60]}', \
                        '{data_list[id+sub_id][6][:40]}', {data_list[id+sub_id][7]}, {data_list[id+sub_id][8]-3*persons_offset}),\n"
        f.write(query)

# autofill Casualty table
with open('data-pickles/casualty.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/casualty_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Casualty \n(name, age, gender, address, deg_of_loss) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"('{persons_list[id+sub_id][0][:40]}', {persons_list[id+sub_id][1]}, {persons_list[id+sub_id][2]}, \
                        '{persons_list[id+sub_id][3][:60]}', {data_list[id+sub_id][1]});\n"
            else:
                query += f"('{persons_list[id+sub_id][0][:40]}', {persons_list[id+sub_id][1]}, {persons_list[id+sub_id][2]}, \
                        '{persons_list[id+sub_id][3][:60]}', {data_list[id+sub_id][1]}),\n"
        f.write(query)

# autofill Government_Representative table
with open('data-pickles/govn_rep.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/govn_cred_fill.sql', 'w+') as f:
    query = "INSERT INTO Govn_Rep_Credentials \n(username, password) \nVALUES\n"
    for id in range(int(record_per_table/4)):
        if id == 0:
            query += f"('{data_list[id][1]}', '{data_list[id][2]}')"
            continue
        query += f",\n('{data_list[id][1]}', '{data_list[id][2]}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/govn_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Government_Representative \n(name, age, gender, address, credentials) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"('{persons_list[persons_offset+id+sub_id][0][:40]}', {persons_list[persons_offset+id+sub_id][1]}, \
                        {persons_list[persons_offset+id+sub_id][2]}, '{persons_list[persons_offset+id+sub_id][3][:60]}', {id});\n"
            else:
                query += f"('{persons_list[persons_offset+id+sub_id][0][:40]}', {persons_list[persons_offset+id+sub_id][1]}, \
                        {persons_list[persons_offset+id+sub_id][2]}, '{persons_list[persons_offset+id+sub_id][3][:60]}', {id}),\n"
        f.write(query)

# autofill Citizen table
with open('data-pickles/citizen.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/citizen_cred_fill.sql', 'w+') as f:
    query = "INSERT INTO Citizen_Credentials \n(username, password) \nVALUES\n"
    for id in range(int(record_per_table/4)):
        if id == 0:
            query += f"('{data_list[id][1]}', '{data_list[id][2]}')"
            continue
        query += f",\n('{data_list[id][1]}', '{data_list[id][2]}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/citizen_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Citizen \n(name, age, gender, address, credentials, trust_level) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"('{persons_list[2*persons_offset+id+sub_id][0][:40]}', {persons_list[2*persons_offset+id+sub_id][1]}, \
                        {persons_list[2*persons_offset+id+sub_id][2]}, '{persons_list[2*persons_offset+id+sub_id][3][:60]}', {id}, {data_list[id][3]});\n"
            else:
                query += f"('{persons_list[2*persons_offset+id+sub_id][0][:40]}', {persons_list[2*persons_offset+id+sub_id][1]}, \
                        {persons_list[2*persons_offset+id+sub_id][2]}, '{persons_list[2*persons_offset+id+sub_id][3][:60]}', {id}, {data_list[id][3]}),\n"
        f.write(query)

# autofill Criminal table
with open('data-pickles/criminal.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/criminal_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Criminal \n(name, age, gender, address, no_of_crimes) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"('{persons_list[3*persons_offset+id+sub_id][0][:40]}', {persons_list[3*persons_offset+id+sub_id][1]}, \
                        {persons_list[3*persons_offset+id+sub_id][2]}, '{persons_list[3*persons_offset+id+sub_id][3][:60]}', {data_list[id+sub_id][1]});\n"
            else:
                query += f"('{persons_list[3*persons_offset+id+sub_id][0][:40]}', {persons_list[3*persons_offset+id+sub_id][1]}, \
                        {persons_list[3*persons_offset+id+sub_id][2]}, '{persons_list[3*persons_offset+id+sub_id][3][:60]}', {data_list[id+sub_id][1]}),\n"
        f.write(query)

# autofill Report table
with open('data-pickles/report.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/report_content_fill.sql', 'w+') as f:
    query = "INSERT INTO Report_Content \n(corpus) \nVALUES\n"
    for id in range(record_per_table):
        text = data_list[id][0].replace("'", "")
        if id == 0:
            query += f"('{text}')"
            continue
        query += f",\n('{text}')"
    query += ";"
    f.write(query)
with open('optimized-sql-scripts/report_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Report \n(content, incident_id, govn_id, citizen_id) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"({id}, {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]-persons_offset}, {data_list[id+sub_id][3]-2*persons_offset});\n"
            else:
                query += f"({id}, {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]-persons_offset}, {data_list[id+sub_id][3]-2*persons_offset}),\n"
        f.write(query)

# autofill Casualty_Incident table
with open('data-pickles/casualty_incident.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('optimized-sql-scripts/casualty_incident_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Casualty_Incident \n(incident_id, casualty_id) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}),\n"
        f.write(query)
