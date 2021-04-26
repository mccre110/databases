import pandas as pd
import mysql.connector
import csv


db = mysql.connector.connect(
    host="35.236.32.138",
    user="root",
    password="testing123",
    database="Students"
)

cur = db.cursor()

def importCSV():
    with open("output.csv") as f:
        input_file = csv.DictReader(f)
        for row in input_file:
            mechanicID = insertMechanic(row)
            makeID = checkExist("Manufacturer", "Name", row["Make"])
            if makeID == 0:
                makeID = insertMake(row)
            modelID = checkExist("Model", "Name", row["Model"])
            if modelID == 0:
                modelID = insertModel(row, makeID)
            vehicleID = insertVehicle(row, modelID)
            invoiceID = insertInvoice(row, mechanicID, vehicleID)


def insertVehicle(row, mID):
    cur.execute('''
            INSERT INTO Vehicle(Year, Color, ModelID)
            VALUES (%s,%s,%s)
            ''',
                (row["Year"],
                 row["Color"],
                 mID)
                )
    db.commit()
    return cur.lastrowid


def insertMake(row):
    cur.execute('''
            INSERT INTO Manufacturer(Name)
            VALUES (%s)
            ''',
                (row["Make"],)
                )
    db.commit()
    return cur.lastrowid


def insertModel(row, mID):
    cur.execute('''
            INSERT INTO Model(Name, ManufacturerID, MPG)
            VALUES (%s,%s,%s)
            ''',
                (row["Model"],
                 mID,
                 row["MPG"])
                )
    db.commit()
    return cur.lastrowid


def insertInvoice(row, mID, vID):
    cur.execute('''
            INSERT INTO Invoice(Date, Amount, MechanicID, Description, Odometer, VehicleID)
            VALUES (%s,%s,%s,%s,%s,%s)
            ''',
                (row["Date"],
                 row["Amount"],
                 mID,
                 row["Desc"],
                 row["Odo"],
                 vID)
                )
    db.commit()
    return cur.lastrowid


def insertMechanic(row):
    cur.execute('''
            INSERT INTO Mechanic(Name, PhoneNumber, Address)
            VALUES (%s,%s,%s)
            ''',
                (row["Mechanic"],
                 row["Phone"],
                 row["Address"])
                )
    db.commit()
    return cur.lastrowid


def checkExist(table, rowName, item):
    cur.execute(
        """SELECT ID FROM %s WHERE %s = '%s'""" %
        (table, rowName, item)
    )

    results = cur.fetchall()
    row_count = cur.rowcount
    if row_count == 0:
        return 0
    else:
        return results[0][0]

importCSV()
