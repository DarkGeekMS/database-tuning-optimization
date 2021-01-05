-- 1) List names and ages of casualties of incidents with economic loss more than 50000
-- Non-optimized
SELECT Person.name, Person.age 
FROM Incident, Casualty_Incident, Casualty, Person
WHERE Incident.id = Casualty_Incident.incident_id and Casualty_Incident.casualty_id = Casualty.id 
    and Casualty.id = Person.id and Incident.eco_loss > 50000;
-- Optimized
SELECT Casualty.name, Casualty.age 
FROM Incident, Casualty_Incident, Casualty
WHERE Incident.id = Casualty_Incident.incident_id and Casualty_Incident.casualty_id = Casualty.id 
    and Incident.eco_loss > 50000;

-- 2) List degree of loss for casualties of disasters that have at least one previous occurance
-- Non-optimized
SELECT deg_of_loss
FROM Disaster, Incident, Casualty_Incident, Casualty
WHERE Disaster.id=Incident.type and Incident.id = Casualty_Incident.incident_id 
    and Casualty_Incident.casualty_id = Casualty.id and Disaster.no_of_prev_occur != 0;
-- Optimized
SELECT deg_of_loss
FROM Disaster, Incident, Casualty_Incident, Casualty
WHERE Disaster.id=Incident.type and Incident.id = Casualty_Incident.incident_id 
    and Casualty_Incident.casualty_id = Casualty.id and Disaster.no_of_prev_occur != 0;

-- 3) List names and dates of incidents that are reported by citizens with trust level more than 5
-- Non-optimized
SELECT Incident.name, Incident.year, Incident.month, Incident.day
FROM Incident, Report, Citizen
WHERE Incident.id = Report.incident_id and Report.citizen_id = Citizen.id
    and Citizen.trust_level > 5;
-- Optimized
SELECT Incident.name, Incident.inc_date
FROM Incident, Report, Citizen
WHERE Incident.id = Report.incident_id and Report.citizen_id = Citizen.id
    and Citizen.trust_level > 5;

-- 4) List information of all criminals involved in disasters with incidents of economic loss less than 50000
-- Non-optimized
SELECT Person.name, Person.age, Person.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Person
WHERE Disaster.id=Incident.type and Incident.suspect = Criminal.id
    and Criminal.id = Person.id and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss < 50000
    );
-- Optimized
SELECT Criminal.name, Criminal.age, Criminal.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal
WHERE Disaster.id=Incident.type and Incident.suspect = Criminal.id
    and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss < 50000
    );

-- 5) List names and economic losses of incidents reported by citizens with an 'a' in their names
-- Non-optimized
SELECT Incident.name, Incident.eco_loss
FROM Report, Citizen, Incident, Person
WHERE Report.citizen_id =  Citizen.id and Report.incident_id = Incident.id and Citizen.id =  Person.id 
    and Person.name LIKE '%a%';
-- Optimized
SELECT Incident.name, Incident.eco_loss
FROM Incident, Report, Citizen
WHERE Report.incident_id = Incident.id and Report.citizen_id =  Citizen.id and Citizen.name LIKE '%a%';
