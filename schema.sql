CREATE DATABASE Disasters_DB;

USE Disasters_DB;

CREATE TABLE Disaster (
  name varchar(40) PRIMARY KEY,
  possible_causes text,
  precautions text,
  no_of_prev_occur int DEFAULT 0
);

CREATE TABLE Incident (
  id int PRIMARY KEY AUTO_INCREMENT,
  eco_loss int DEFAULT 0,
  year int NOT NULL,
  month int NOT NULL,
  day int NOT NULL,
  description text,
  location varchar(60) NOT NULL,
  name varchar(40),
  type varchar(40)
);

CREATE TABLE Person (
  ssn varchar(14) PRIMARY KEY,
  name varchar(40) NOT NULL,
  age int,
  gender int,
  address varchar(60)
);

CREATE TABLE Casualty (
  ssn varchar(14) PRIMARY KEY,
  deg_of_loss varchar(10) NOT NULL
);

CREATE TABLE Government_Representative (
  ssn varchar(14) PRIMARY KEY,
  username varchar(40) NOT NULL,
  password varchar(60) NOT NULL,
  data_of_join datetime DEFAULT (CURRENT_TIMESTAMP())
);

CREATE TABLE Citizen (
  ssn varchar(14) PRIMARY KEY,
  username varchar(40) NOT NULL,
  password varchar(60) NOT NULL,
  data_of_join datetime DEFAULT (CURRENT_TIMESTAMP()),
  trust_level int NOT NULL DEFAULT 0
);

CREATE TABLE Report (
  report_id int PRIMARY KEY AUTO_INCREMENT,
  content text NOT NULL,
  report_date datetime DEFAULT (CURRENT_TIMESTAMP()),
  incident_id int,
  govn_ssn varchar(14),
  citizen_ssn varchar(14)
);

CREATE TABLE Casualty_Incident (
  incident_id int,
  casualty_ssn varchar(14),
  primary key (incident_id, casualty_ssn)
);

ALTER TABLE Incident ADD FOREIGN KEY (type) REFERENCES Disaster (name) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Casualty ADD FOREIGN KEY (ssn) REFERENCES Person (ssn) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Government_Representative ADD FOREIGN KEY (ssn) REFERENCES Person (ssn) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE Citizen ADD FOREIGN KEY (ssn) REFERENCES Person (ssn) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Report ADD FOREIGN KEY (incident_id) REFERENCES Incident (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Report ADD FOREIGN KEY (govn_ssn) REFERENCES Government_Representative (ssn) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE Report ADD FOREIGN KEY (citizen_ssn) REFERENCES Citizen (ssn) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE Casualty_Incident ADD FOREIGN KEY (incident_id) REFERENCES Incident (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Casualty_Incident ADD FOREIGN KEY (casualty_ssn) REFERENCES Casualty (ssn) ON DELETE CASCADE ON UPDATE CASCADE;
