----------------------------------------------------------------------------------------------------
-- filter not-needed conditions (satisfied by other conditions or impossible to happen)

-- non-optimized
SELECT Person.name, Person.age, Person.gender, Criminal.no_of_crimes
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
        WHERE Disaster.id=Incident.type and Incident.eco_loss < 50000 
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


-- optimized
SELECT Person.name, Person.age, Person.gender, Criminal.no_of_crimes
FROM Disaster, Incident, Criminal, Person, Report
    WHERE Disaster.id=Incident.type 
    and Incident.suspect = Criminal.id 
    and Incident.id = Report.incident_id 
    and Criminal.id = Person.id 

    and Disaster.id IN (
        SELECT Disaster.id
        FROM Disaster, Incident
        WHERE Disaster.id=Incident.type and Incident.eco_loss < 50000 
    )
;


----------------------------------------------------------------------------------------------------
-- INDEX TUNING (i.e. UNION is Better than OR when there's index for different conditions)
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

-- before added indexes -- optimal --
SELECT Incident.id
FROM Incident
    WHERE (Incident.year = 2010 or Incident.month = 9 or Incident.day = 20 or Incident.eco_loss = 100000)
    ;

-- index adding
CREATE INDEX Incident_month_Idx ON Incident(month);
CREATE INDEX Incident_year_Idx ON Incident(year);
CREATE INDEX Incident_day_Idx ON Incident(day);
CREATE INDEX Incident_eco_loss_Idx ON Incident(eco_loss);

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

-- remove added indexes
DROP INDEX Incident_month_Idx ON Incident;
DROP INDEX Incident_year_Idx ON Incident;
DROP INDEX Incident_day_Idx ON Incident;
DROP INDEX Incident_eco_loss_Idx ON Incident;
----------------------------------------------------------------------------------------------------


