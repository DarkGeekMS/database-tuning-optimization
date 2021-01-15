-- for Memory optimization we update the InnoDB Buffer pool size with different values and compared the results (default value = 134217728 )
-- default time on Query 1 ->
    -- 1st -> 1.53 sec
    -- 2nd -> 0.68 sec
    -- 3rd -> 
-- default time on Query 3 ->
    -- 1st -> 0.09 sec
    -- 2nd -> 0.07 sec
    -- 3rd -> 0.01 sec
-- default time on Query 4 ->
    -- 1st -> 0.43 sec
    -- 2nd ->
-- default time on Query 5 ->
    -- 1st -> 0.51 sec
    -- 2nd ->
    -- 3rd -> 0.39 sec
    -- 4th ->
---------------------------------------------------------------------------------------------------------

-- set the buffer size to 2GB( 2147483648 ).
-- effect on Query 1 ->
    -- 1st -> 1.16 sec
    -- 2nd -> 0.69 sec
    -- 3rd -> 
-- effect on Query 3 ->
    -- 1st -> 0.08 sec
    -- 2nd -> 0.06 sec
    -- 3ed -> 0.05 sec
-- effect on Query 4 ->
    -- 1st -> 0.27 sec
    -- 2nd -> 
-- effect on Query 5 ->
    -- 1st -> 0.56 sec
    -- 2nd ->
    -- 3rd -> 0.28 sec
    -- 4th ->


SET GLOBAL innodb_buffer_pool_size=2147483648;  


-- set the buffer size to 4G(402653184). 
-- effect on Query 1 ->
    -- 1st -> 1.26 sec
    -- 2nd -> 0.6 sec
    -- 3rd -> 
-- effect on Query 3 ->
    -- 1st -> 0.08 sec
    -- 2nd -> 0.04 sec
    -- 3ed -> 0.04 sec
-- effect on Query 4 ->
    -- 1st -> 0.33 sec
    -- 2nd -> 
-- effect on Query 5 ->
    -- 1st -> 0.43 sec
    -- 2nd ->
    -- 3rd -> 0.35 sec
    -- 4th ->

SET GLOBAL innodb_buffer_pool_size=402653184;  




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

-- OLD SCHEMA --> time = 0.18 sec
-- optimized on old schema
SELECT Incident.name, Person.name, Person.age, Person.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Person
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Criminal.id = Person.id 
    and Incident.eco_loss > 50000;

-- NEW SCHEMA --> time = 0.14 sec
-- optimized on new schema
-- TODO : NoSQL Implementation
SELECT Incident.name, Criminal.name, Criminal.age, Criminal.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Incident.eco_loss > 50000;

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

-- NEW or OLD SCHEMA --> time = 9 mins - 39 secs
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

-- OLD SCHEMA --> time = 0.93 sec
-- NEW SCHEMA --> time = 0.82 sec
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

-- OLD SCHEMA --> time = 0.81 sec
-- NEW SCHEMA --> time = 0.72 sec
-- second optimization using UNION ALL instead of UNION
-- TODO : NoSQL Implementation
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

-- NEW or OLD SCHEMA --> time = 0.07 sec
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

-- NEW or OLD SCHEMA --> time = 0.03 sec
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

-- OLD SCHEMA --> time = 0.01 sec
-- NEW SCHEMA --> time = 0.00 sec
-- after added indexes -- optimal --
-- TODO : NoSQL Implementation
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
-- Query 4
----------------------------------------------------------------------------------------------------
-- SCHEMA OPTIMIZATION
-- QUERY REWRITING
/* Query gets the name, date, economic loss and report id of incident whose report is submitted by a female citizen
    to a male government representative
*/

-- OLD SCHEMA --> time = 0.27 sec
-- unoptimized
SELECT Incident.name, Incident.year, Incident.month, Incident.day, Incident.eco_loss, Report.id
FROM Incident, Report
WHERE Incident.id = Report.incident_id
and Report.citizen_id IN (
    SELECT Citizen.id
    FROM Citizen, Person
    WHERE Citizen.id = Person.id and Person.gender = 0
)
and Report.govn_id IN (
    SELECT Government_Representative.id
    FROM Government_Representative, Person
    WHERE Government_Representative.id = Person.id and Person.gender = 1
);

-- NEW SCHEMA --> time = 0.17 sec
-- optimized
-- TODO : NoSQL Implementation
SELECT Incident.name, Incident.year, Incident.month, Incident.day, Incident.eco_loss, Report.id
FROM Incident, Report, Citizen, Government_Representative
WHERE Incident.id = Report.incident_id
and Report.citizen_id = Citizen.id and Report.govn_id = Government_Representative.id
and Citizen.gender = 0 and Government_Representative.gender = 1;

----------------------------------------------------------------------------------------------------
-- Query 5
----------------------------------------------------------------------------------------------------
-- SCHEMA OPTIMIZATION
-- QUERY REWRITING
/* Query gets the name of incident and the information of involved casualties
    where suspect at least one crime and economic loss less than 50000 and disaster type
    with at least one previous occurance
    1) redundant condition on number of crimes
    2) ranges are slower than inequalities in sql
    3) not equal is slower than inequality in sql
*/

-- OLD SCHEMA --> time = 0.39 sec
-- unoptimized
SELECT Incident.name, Person.name, Person.age, Person.gender, Person.address
FROM Disaster, Incident, Casualty_Incident, Casualty, Person
WHERE Disaster.id = Incident.type and Incident.id = Casualty_Incident.incident_id
and Casualty_Incident.casualty_id = Casualty.id
and Casualty.id = Person.id and Incident.suspect IN (
    SELECT Criminal.id
    FROM Criminal, Person
    WHERE Criminal.id = Person.id and Criminal.no_of_crimes > 0
) and Incident.eco_loss BETWEEN 0 AND 50000
and Disaster.no_of_prev_occur != 0;

-- NEW SCHEMA --> time = 0.31 sec
-- unoptimized
SELECT Incident.name, Casualty.name, Casualty.age, Casualty.gender, Casualty.address
FROM Disaster, Incident, Casualty_Incident, Casualty
WHERE Disaster.id = Incident.type and Incident.id = Casualty_Incident.incident_id
and Casualty_Incident.casualty_id = Casualty.id
and Incident.suspect IN (
    SELECT id
    FROM Criminal
    WHERE no_of_crimes > 0
) and Incident.eco_loss BETWEEN 0 AND 50000
and Disaster.no_of_prev_occur != 0;

-- OLD SCHEMA --> time = 0.26 sec
-- optimized
SELECT Incident.name, Person.name, Person.age, Person.gender, Person.address
FROM Disaster, Incident, Casualty_Incident, Casualty, Person
WHERE Disaster.id = Incident.type and Incident.id = Casualty_Incident.incident_id
and Casualty_Incident.casualty_id = Casualty.id
and Casualty.id = Person.id and Incident.eco_loss < 50000
and Disaster.no_of_prev_occur > 0;

-- NEW SCHEMA --> time = 0.23 sec
-- optimized
-- TODO : NoSQL Implementation
SELECT Incident.name, Casualty.name, Casualty.age, Casualty.gender, Casualty.address
FROM Disaster, Incident, Casualty_Incident, Casualty
WHERE Disaster.id = Incident.type and Incident.id = Casualty_Incident.incident_id
and Casualty_Incident.casualty_id = Casualty.id
and Incident.eco_loss < 50000 and Disaster.no_of_prev_occur > 0;
