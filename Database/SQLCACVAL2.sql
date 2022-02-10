use PI2;
#drop table Equity;

CREATE TABLE IF NOT EXISTS Equity (Equity_Name VARCHAR(40) NOT NULL,PRIMARY KEY (Equity_Name) ) ; 

CREATE TABLE IF NOT EXISTS Stock (Stock_Date DATE,
 Stock_Value DOUBLE, 
 Equity_Name VARCHAR(40) NOT NULL, PRIMARY KEY (Stock_Date,Equity_Name),
 FOREIGN KEY (Equity_Name) REFERENCES Equity(Equity_Name)); 

#INSERT INTO Titre(Titre_Nom) VALUES("test");

select * from Stock;
#drop table Stock;

DELETE FROM Equity WHERE Equity_name ="Date";
select count(*) from Stock;
select * from Stock;
select Stock_Date,Equity_Name, Stock_Value from Stock join Equity using(Equity_Name) group by Equity_Name;