CREATE DATABASE IF NOT EXISTS Price;
USE Price;
#pas de maj pour col et table
CREATE TABLE IF NOT EXISTS Titre (Titre_Nom VARCHAR(40) NOT NULL,PRIMARY KEY (Titre_Nom) ) ; 
#d_date #t(type)_namecolumn
CREATE TABLE IF NOT EXISTS Donnee (Donnee_Date DATE,
 Donnee_Value DOUBLE, 
 Titre_Nom VARCHAR(40) NOT NULL, PRIMARY KEY (Donnee_Date,Titre_Nom),
 FOREIGN KEY (Titre_Nom) REFERENCES Titre(Titre_nom)); 

INSERT INTO Titre(Titre_Nom) VALUES("test");

select * from Donnee;
drop table Donnee;

DELETE FROM Titre WHERE Titre_Nom ="Date";