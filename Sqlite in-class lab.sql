-- 1.Write a query to retrieve FirstName, Last Name and email from the Employee table
select FirstName, LastName, Email from Employee;

-- 2.Write a query to retrieve all records in the Artists table
select * from Artist;

-- 3.Write a query to retrieve all Employees who are a manager(i.e. manager is in their job title)
select * from Employee where Title like '%Manager%';

-- 4.Write a query to retrieve the largest and smallest Invoice
--select * from Invoice group by desc Total;

-- 5.Write a query to retrieve all invoices for Germany with the following columns: BillingAddress, BillingCity, BillingPostalCode and Invoice Total
select BillingAddress, BillingCity, BillingPostalCode, Total from Invoice where BillingCountry = 'Germany';

-- 6.Write a query to retrieve all invoices where the total is between $15 and $25with the following columns: BillingAddress, BillingCity, BillingPostalCode and Invoice Total
select BillingAddress, BillingCity, BillingPostalCode, Total from Invoice where Total > 15 AND Total<25;

-- 7.Provide a query showing a unique list of billing countries from the Invoice table.
select distinct BillingCountry from Invoice;

-- 8.Provide a query showing Customers (just their full names, customer ID and country) who are not in the US.
select  FirstName, LastName, CustomerId, Country from Customer where Country <> 'USA';

-- 9.Provide a query only showing the Customers from Brazil.
select * from Customer where Country = 'Brazil';

-- 10.Provide a query that includes the track name with each invoice line item and sort by track name
select Track.Name, InvoiceLine.* from Track join InvoiceLine on Track.TrackId = InvoiceLine.TrackId ORDER BY Track.Name;