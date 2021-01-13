-- QUERY 1
----------------------------------------------------------------------------------------------------
-- filter not-needed conditions (satisfied by other conditions or impossible not to happen)
/* Meaning: Query to get all Criminals that  
    1- are males or females (i.e. No OTHERS here)
    2- belong to a disaster that has an incident with eco loss higher than 50000
    3- his crime is reviewed by a Government Representative that is older than 10 years old (No KIDS here)
    4- is reported by a citizen whose trust level is not higher than 10 
*/

-- OLD SCHEMA --> time = 1.81 sec
-- non-optimized
SELECT Incident.name, Person.name, Person.age, Person.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Person, Report
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Incident.id = Report.incident_id 
    and Criminal.id = Person.id 
    -- can be removed (i.e. no OTHERS here)
    and Person.gender IN (0,1)
    and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss > 50000 
    )
    -- can be removed (i.e. no Government Representatives less than or equal 10 years old)
    and Report.govn_id IN (
        SELECT Government_Representative.id
        FROM Government_Representative, Person
        WHERE Person.id=Government_Representative.id and (Person.age > 10 )
    )
    -- can be removed (i.e. trust levels are of maximum = 10)
    and Report.citizen_id IN (
        SELECT Citizen.id
        FROM Citizen
        WHERE (Citizen.trust_level <= 10)
    )
;

-- OLD SCHEMA --> time = 0.58 sec
-- optimized on old schema
SELECT Incident.name, Person.name, Person.age, Person.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Person, Report
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Incident.id = Report.incident_id 
    and Criminal.id = Person.id 
    and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss > 50000 
    )
;

-- NEW SCHEMA --> 0.49 sec
-- optimized on new schema
SELECT Incident.name, Criminal.name, Criminal.name, Criminal.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Report
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Incident.id = Report.incident_id 
    and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss > 50000 
    )
;

----------------------------------------------------------------------------------------------------
-- QUERY 2
----------------------------------------------------------------------------------------------------
-- Index Tuning on Incident.name
-- UNION ALL vs UNION
/* Meaning: Query to get all Incidents that  
    1- have a criminal with number of crimes less than 10
    2- belong to a disaster with number of previous occurences higher than 10
    3- have a name identical to an incident's name with year = 2010, month = 9, day = 20 or eco_loss = 100000
*/

-- NEW or OLD SCHEMA --> 9 mins - 39 secs
-- non-optimized query (i.e. before indexes and with UNION)
SELECT Incident.id, Incident.suspect, Incident.type
FROM Incident, Disaster, Criminal
WHERE Incident.name IN (
    SELECT Incident.name
    FROM Incident
        WHERE Incident.year = 2010
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.month = 9
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.day = 20
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.eco_loss = 100000
)
and Incident.type = Disaster.id
and Incident.suspect = Criminal.id
and Disaster.no_of_prev_occur > 10
and Criminal.no_of_crimes < 10
;

-- NEW or OLD SCHEMA
-- first optimization (i.e. add index on Incident.name)
CREATE INDEX Incident_name_Idx ON Incident(name);

-- OLD SCHEMA --> 0.93 sec
-- NEW SCHEMA --> 0.82 sec
-- optimized query (same non-optimized but with index on Incident.name now)
SELECT Incident.id, Incident.suspect, Incident.type
FROM Incident, Disaster, Criminal
WHERE Incident.name IN (
    SELECT Incident.name
    FROM Incident
        WHERE Incident.year = 2010
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.month = 9
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.day = 20
    UNION 
    SELECT Incident.name
    FROM Incident
        WHERE Incident.eco_loss = 100000
)
and Incident.type = Disaster.id
and Incident.suspect = Criminal.id
and Disaster.no_of_prev_occur > 10
and Criminal.no_of_crimes < 10
;

-- OLD SCHEMA --> 0.81 sec
-- NEW SCHEMA --> 0.72 sec
-- second optimization using UNION ALL instead of UNION
SELECT Incident.id, Incident.suspect, Incident.type
FROM Incident, Disaster, Criminal
WHERE Incident.name IN (
    SELECT Incident.name
    FROM Incident
        WHERE Incident.year = 2010
    UNION ALL
    SELECT Incident.name
    FROM Incident
        WHERE Incident.month = 9
    UNION ALL
    SELECT Incident.name
    FROM Incident
        WHERE Incident.day = 20
    UNION ALL
    SELECT Incident.name
    FROM Incident
        WHERE Incident.eco_loss = 100000
)
and Incident.type = Disaster.id
and Incident.suspect = Criminal.id
and Disaster.no_of_prev_occur > 10
and Criminal.no_of_crimes < 10
;

-- NEW or OLD SCHEMA
-- Drop indexes
DROP INDEX Incident_name_Idx ON Incident;

----------------------------------------------------------------------------------------------------
-- QUERY 3
----------------------------------------------------------------------------------------------------
-- INDEX TUNING (i.e. UNION is Better than OR when there're indexes for different conditions)
/* Meaning: Query to get all Incidents that is with
     year = 2010 
     or 
     month = 9 
     or
     day = 20 
     or
     eco_loss = 100000
*/

-- NEW or OLD SCHEMA --> 0.07 sec
-- before added indexes -- non-optimal --
SELECT Incident.id
FROM Incident
    WHERE Incident.year = 2010
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.month = 9
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.day = 20
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.eco_loss = 100000;

-- NEW or OLD SCHEMA --> 0.03 sec
-- before added indexes -- optimal --
SELECT Incident.id
FROM Incident
    WHERE (Incident.year = 2010 or Incident.month = 9 or Incident.day = 20 or Incident.eco_loss = 100000)
    ;

-- NEW or OLD SCHEMA
-- index adding
CREATE INDEX Incident_month_Idx ON Incident(month);
CREATE INDEX Incident_year_Idx ON Incident(year);
CREATE INDEX Incident_day_Idx ON Incident(day);
CREATE INDEX Incident_eco_loss_Idx ON Incident(eco_loss);

-- OLD SCHEMA --> 0.01 sec
-- NEW SCHEMA --> 0.00 sec
-- after added indexes -- optimal --
SELECT Incident.id
FROM Incident
    WHERE Incident.year = 2010
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.month = 9
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.day = 20
UNION
SELECT Incident.id
FROM Incident
    WHERE Incident.eco_loss = 100000;

-- NEW or OLD SCHEMA
-- Drop indexes
DROP INDEX Incident_month_Idx ON Incident;
DROP INDEX Incident_year_Idx ON Incident;
DROP INDEX Incident_day_Idx ON Incident;
DROP INDEX Incident_eco_loss_Idx ON Incident;

----------------------------------------------------------------------------------------------------
