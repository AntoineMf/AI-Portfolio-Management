DROP DATABASE IF EXISTS Price;
CREATE DATABASE IF NOT EXISTS Price;
USE Price;

  
DROP TABLE IF EXISTS Donnée ; 
CREATE TABLE Donnée (Donnée_Date DATE NOT NULL, Donnée_Value_Fermeture DOUBLE,
 Donnée_Value_Ouverture DOUBLE, Donnée_Value_Max DOUBLE, Donnée_Value_Min DOUBLE, 
 Donnée_Volume DOUBLE, Donnée_Variation DOUBLE, 
 Titre_Nom VARCHAR(40) NOT NULL, PRIMARY KEY (Donnée_Date) ) ENGINE=InnoDB; 

DROP TABLE IF EXISTS Titre ; 
CREATE TABLE Titre (Titre_Nom VARCHAR(40) NOT NULL, Titre_Poid DOUBLE, PRIMARY KEY (Titre_Nom) ) ENGINE=InnoDB;  

ALTER TABLE Donnée ADD CONSTRAINT FK_Donnée_Titre_Nom FOREIGN KEY (Titre_Nom) REFERENCES Titre (Titre_Nom); 