"""
This script is used to convert data pickles into sql queries
"""
import pickle
import sys

# number of records per table
record_per_table = int(sys.argv[1])

# autofill Disaster table
with open('data-pickles/disaster.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/disaster_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Disaster \n(name, possible_causes, precautions, no_of_prev_occur) \nVALUES\n"
        for sub_id in range(1000):
            name = data_list[id+sub_id][0][:40].replace("'", "")
            causes = data_list[id+sub_id][1].replace("'", "")
            precautions = data_list[id+sub_id][2].replace("'", "")
            if sub_id == 999:
                query += f"('{name}', '{causes}', '{precautions}', {data_list[id+sub_id][3]});\n"
            else:
                query += f"('{name}', '{causes}', '{precautions}', {data_list[id+sub_id][3]}),\n"
        f.write(query)
            
# autofill Incident table
with open('data-pickles/incident.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/incident_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Incident (year, month, day, description, eco_loss, location, name, type, suspect) \nVALUES\n"
        for sub_id in range(1000):
            name = data_list[id+sub_id][5][:40].replace("'", "")
            description = data_list[id+sub_id][3].replace("'", "")
            if sub_id == 999:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, \
                        '{description}', {data_list[id+sub_id][4]}, '{name}', \
                        '{data_list[id+sub_id][6]}', {data_list[id+sub_id][7]}, {data_list[id+sub_id][8]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, \
                        '{description}', {data_list[id+sub_id][4]}, '{name}', \
                        '{data_list[id+sub_id][6]}', {data_list[id+sub_id][7]}, {data_list[id+sub_id][8]}),\n"
        f.write(query)

# autofill Person table
with open('data-pickles/person.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/person_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Person \n(name, age, gender, address) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"('{data_list[id+sub_id][0][:40]}', {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, '{data_list[id+sub_id][3][:60]}');\n"
            else:
                query += f"('{data_list[id+sub_id][0][:40]}', {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, '{data_list[id+sub_id][3][:60]}'),\n"
        f.write(query)

# autofill Casualty table
with open('data-pickles/casualty.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/casualty_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Casualty \n(id, deg_of_loss) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}),\n"
        f.write(query)

# autofill Government_Representative table
with open('data-pickles/govn_rep.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/govn_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Government_Representative \n(id, username, password) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"({data_list[id+sub_id][0]}, '{data_list[id+sub_id][1][:40]}', '{data_list[id+sub_id][2][:60]}');\n"
            else:
                query += f"({data_list[id+sub_id][0]}, '{data_list[id+sub_id][1][:40]}', '{data_list[id+sub_id][2][:60]}'),\n"
        f.write(query)

# autofill Citizen table
with open('data-pickles/citizen.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/citizen_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Citizen \n(id, username, password, trust_level) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"({data_list[id+sub_id][0]}, '{data_list[id+sub_id][1][:40]}', '{data_list[id+sub_id][2][:60]}', {data_list[id+sub_id][3]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, '{data_list[id+sub_id][1][:40]}', '{data_list[id+sub_id][2][:60]}', {data_list[id+sub_id][3]}),\n"
        f.write(query)

# autofill Criminal table
with open('data-pickles/criminal.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/criminal_fill.sql', 'w+') as f:
    for id in range(0, int(record_per_table/4), 1000):
        query = "INSERT INTO Criminal \n(id, no_of_crimes) \nVALUES\n"
        for sub_id in range(1000):
            if id+sub_id == int(record_per_table/4):
                break
            if sub_id == 999 or id+sub_id == int(record_per_table/4)-1:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}),\n"
        f.write(query)

# autofill Report table
with open('data-pickles/report.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/report_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Report \n(content, incident_id, govn_id, citizen_id) \nVALUES\n"
        for sub_id in range(1000):
            content = data_list[id+sub_id][0].replace("'", "")
            if sub_id == 999:
                query += f"('{content}', {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, {data_list[id+sub_id][3]});\n"
            else:
                query += f"('{content}', {data_list[id+sub_id][1]}, {data_list[id+sub_id][2]}, {data_list[id+sub_id][3]}),\n"
        f.write(query)

# autofill Casualty_Incident table
with open('data-pickles/casualty_incident.pkl', 'rb') as f:
    data_list = pickle.load(f)
with open('sql-scripts/casualty_incident_fill.sql', 'w+') as f:
    for id in range(0, record_per_table, 1000):
        query = "INSERT INTO Casualty_Incident \n(incident_id, casualty_id) \nVALUES\n"
        for sub_id in range(1000):
            if sub_id == 999:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]});\n"
            else:
                query += f"({data_list[id+sub_id][0]}, {data_list[id+sub_id][1]}),\n"
        f.write(query)
