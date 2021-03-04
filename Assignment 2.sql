-- 1. Create a table Player with the following attributes. You will also define what the data types are going to be.
CREATE TABLE Player (
    pID smallint unsigned not null,
    name varchar(60) not null,
    teamName varchar(60),
    PRIMARY KEY (pID)
);

-- 2. Alter the Player table to add a new column, age.
ALTER TABLE Player
ADD age smallint unsigned;

-- 3. Insert the following tuples into the table:
INSERT INTO Player (pID, name, teamName,age)
VALUES (1,'Player 1', 'Team A',23),
        (3, 'Player 3','Team B',28);

INSERT INTO Player (pID, name, teamName)
VALUES (2,'Player 2', 'Team A'),
        (4, 'Player 4','Team B');

-- 4. Update the table to delete Player 2’s record from it.
DELETE from Player where pID = 2;

-- 5. Update the table to set age = 25 for tuples where age attribute is NULL.
UPDATE Player Set age = 25 where age is NULL;

-- 6. Write a query to return the number of tuples and average age from the Player table.
SELECT count(*),AVG(age) from Player;

-- 7. Drop the player table
DROP TABLE Player;

-- 8. Write a query to return the average Total of invoices where the billing country is Brazil.
select AVG(Total) from Invoice where BillingCountry is 'Brazil';

-- 9. Write a query to return the average Total per billing city of invoices where the billing country is Brazil.
select BillingCity,AVG(Total) from Invoice where BillingCountry is 'Brazil' group by BillingCity;

-- 10. Write a query to return the names of all albums which have a more than 20 tracks.
select Album.Title "Album Name", count(*) from Album,Track where Album.AlbumId = Track.AlbumId group by Album.Title having count(*) > 20;

-- 11. Write a query to show how many invoices were processed in the year 2010.
select count(*) from Invoice where InvoiceDate like '2010%';

-- 12. Write a query to answer how many distinct billing cities there are per each billing country.
select count(distinct BillingCity),BillingCountry from Invoice group by BillingCountry;

-- 13. Write a query to show the album title, track name, and media type name for each record.
select Album.Title 'Album Title', Track.Name, MediaType.Name
from Track,Album,MediaType
where Track.AlbumId = Album.AlbumId and Track.MediaTypeId = MediaType.MediaTypeId;

-- 14. Write a query to find how many sales(invoice count)did Jane Peacock make as a support representative.
-- In the Customers table, you will find that SupportRepId maps to an employeeID in the Employees table that you can use.
-- I recommend using a subquery for this.
select count(*) from Invoice where CustomerId in (
    select CustomerId from Customer where SupportRepId in (
        select EmployeeId from Employee where FirstName is 'Jane' and LastName is 'Peacock'
        )
    );

