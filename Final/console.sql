CREATE TABLE StudentTable(
    StudentId INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    Major VARCHAR(30),
    GPA REAL
);

ALTER TABLE Invoice ADD COLUMN isDeleted smallint UNSIGNED DEFAULT 0;
ALTER TABLE Mechanic ADD COLUMN isDeleted smallint UNSIGNED DEFAULT 0;
ALTER TABLE Model DROP COLUMN MPG;

CREATE VIEW VehicleView
AS
SELECT Vehicle.ID as ID, Year, M.Name AS Model, M2.Name AS Make, Color, Vehicle.Miles as Miles
FROM
     Vehicle
         join
            Model M on M.ID = Vehicle.ModelID
         join
            Manufacturer M2 on M.ManufacturerID = M2.ID
WHERE Vehicle.isDeleted != 1;

CREATE VIEW MechanicView
AS
SELECT ID, Name, PhoneNumber, Address
FROM
     Mechanic
WHERE Mechanic.isDeleted != 1;


SELECT * from MechanicView;

CREATE VIEW InvoiceView
AS
SELECT Invoice.ID AS ID, Date, Amount, M.Name, Description
FROM
     Invoice
        join Mechanic M on M.ID = Invoice.MechanicID
        join Vehicle V on V.ID = Invoice.VehicleID
WHERE Invoice.isDeleted != 1;

SELECT * from InvoiceView;

drop database Students;
create database Students;
CREATE TABLE Vehicle(
    ID int auto_increment not null primary key,
    Color varchar(255),
    ModelID int,
    Year int unsigned,
    FOREIGN KEY (ModelID) references Model(ID)
);

CREATE TABLE Model(
    ID int auto_increment not null primary key,
    Name varchar(255),
    ManufacturerID int,
    MPG int unsigned,
    FOREIGN KEY (ManufacturerID) references Manufacturer(ID)
);

CREATE TABLE Manufacturer(
    ID int auto_increment not null primary key,
    Name varchar(255)
);

CREATE TABLE Invoice(
    ID int auto_increment not null primary key,
    Date date,
    Amount double,
    MechanicID int,
    Description varchar(255),
    Odometer int unsigned,
    VehicleID int,
    FOREIGN KEY (VehicleID) references Vehicle(ID),
    FOREIGN KEY (MechanicID) references Mechanic(ID)
);

CREATE TABLE Mechanic(
    ID int auto_increment not null primary key,
    Name varchar(255),
    PhoneNumber varchar(255),
    Address varchar(255)
);

UPDATE `Invoice` SET isDeleted = 0 WHERE ID = 1;

SELECT * FROM Invoice WHERE MechanicID IN
(SELECT MechanicID FROM Invoice WHERE MechanicID = 1 AND VehicleID = 1);


SELECT MechanicID FROM Invoice WHERE MechanicID = 1 AND VehicleID = 1;

SELECT V.Year, M2.Name AS Make, M3.Name AS Model, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
FROM
     Invoice
        join Mechanic M on M.ID = Invoice.MechanicID
        join Vehicle V on V.ID = Invoice.VehicleID
        join Model M2 on V.ModelID = M2.ID
        join Manufacturer M3 on M3.ID = M2.ManufacturerID
WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
GROUP BY V.ID;

SELECT M.Name AS Mechanic, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
FROM
     Invoice
        join Mechanic M on M.ID = Invoice.MechanicID
        join Vehicle V on V.ID = Invoice.VehicleID
        join Model M2 on V.ModelID = M2.ID
        join Manufacturer M3 on M3.ID = M2.ManufacturerID
WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
GROUP BY M.ID;

SELECT M3.Name AS Manufactuer, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
FROM
     Invoice
        join Mechanic M on M.ID = Invoice.MechanicID
        join Vehicle V on V.ID = Invoice.VehicleID
        join Model M2 on V.ModelID = M2.ID
        join Manufacturer M3 on M3.ID = M2.ManufacturerID
WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
GROUP BY M3.ID;

Create UNIQUE INDEX Make_Name_Index On Manufacturer (Name);
Alter TABLE Manufacturer ADD INDEX (Name);
Create UNIQUE INDEX Mechanic_Name_Index On Mechanic (Name);
Alter TABLE Mechanic ADD INDEX (Name);
Create UNIQUE INDEX Model_Name_Index On Model (Name);
Alter TABLE Model ADD INDEX (Name);
Create  INDEX Vehicle_Year_Index On Vehicle (Year);
Alter TABLE Vehicle ADD INDEX (Year);

