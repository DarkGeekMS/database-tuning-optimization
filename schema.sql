CREATE DATABASE Disasters_DB;

USE Disasters_DB;

CREATE TABLE Disaster (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(40) UNIQUE,
  possible_causes text,
  precautions text,
  no_of_prev_occur int DEFAULT 0
);

CREATE TABLE Incident (
  id int PRIMARY KEY AUTO_INCREMENT,
  year int NOT NULL,
  month int NOT NULL,
  day int NOT NULL,
  description text,
  eco_loss int DEFAULT 0,
  location varchar(60) NOT NULL,
  name varchar(40),
  type int,
  suspect int
);

CREATE TABLE Person (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(40) NOT NULL,
  age int,
  gender int,
  address varchar(60)
);

CREATE TABLE Casualty (
  id int PRIMARY KEY,
  deg_of_loss int DEFAULT 1
);

CREATE TABLE Government_Representative (
  id int PRIMARY KEY,
  username varchar(40) NOT NULL,
  password varchar(60) NOT NULL,
  data_of_join datetime DEFAULT (CURRENT_TIMESTAMP())
);

CREATE TABLE Citizen (
  id int PRIMARY KEY,
  username varchar(40) NOT NULL,
  password varchar(60) NOT NULL,
  data_of_join datetime DEFAULT (CURRENT_TIMESTAMP()),
  trust_level int NOT NULL DEFAULT 0
);

CREATE TABLE Criminal (
    id int PRIMARY KEY,
    no_of_crimes int DEFAULT 1
);

CREATE TABLE Report (
  id int PRIMARY KEY AUTO_INCREMENT,
  content text NOT NULL,
  report_date datetime DEFAULT (CURRENT_TIMESTAMP()),
  incident_id int,
  govn_id int,
  citizen_id int
);

CREATE TABLE Casualty_Incident (
  incident_id int,
  casualty_id int,
  PRIMARY KEY (incident_id, casualty_id)
);

ALTER TABLE Incident ADD FOREIGN KEY (type) REFERENCES Disaster (id) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Incident ADD FOREIGN KEY (suspect) REFERENCES Criminal (id) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Casualty ADD FOREIGN KEY (id) REFERENCES Person (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Government_Representative ADD FOREIGN KEY (id) REFERENCES Person (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Citizen ADD FOREIGN KEY (id) REFERENCES Person (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Criminal ADD FOREIGN KEY (id) REFERENCES Person (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Report ADD FOREIGN KEY (incident_id) REFERENCES Incident (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Report ADD FOREIGN KEY (govn_id) REFERENCES Government_Representative (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE Report ADD FOREIGN KEY (citizen_id) REFERENCES Citizen (id) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Casualty_Incident ADD FOREIGN KEY (incident_id) REFERENCES Incident (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Casualty_Incident ADD FOREIGN KEY (casualty_id) REFERENCES Casualty (id) ON DELETE CASCADE ON UPDATE CASCADE;
