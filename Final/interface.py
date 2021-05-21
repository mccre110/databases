from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import mysql.connector
from mysql.connector.errors import DatabaseError
import pandas as pd


class Interface(QObject):

    def __init__(self, parent):
        super(Interface, self).__init__()
        self.parent = parent
        self.db = mysql.connector.connect(
        host="35.236.32.138",
        user="root",
        password="testing123",
        database="Students"
        )
        self.cur = self.db.cursor()

    @pyqtSlot(str)
    def getAll(self, table):
        try:
            self.cur.execute("""SELECT * FROM `%s`;""" % (table,))
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            # df.set_index('ID', inplace=True)
            self.parent.viewSignal.emit(df)
            self.parent.logSignal.emit("""SELECT * FROM `%s`;""" % (table,))
        except DatabaseError:
            print("Error Occured")
    
    @pyqtSlot(str)
    def fetch(self, idx, table):
        try:
            self.cur.execute("""SELECT * FROM `%s` WHERE ID = %s;""" % (table,idx))
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            self.parent.logSignal.emit("""SELECT * FROM `%s` WHERE ID = %s;""" % (table,idx))
            return pd.DataFrame(myrecords, columns=names)
        except DatabaseError:
            print("Error Occured")

    @pyqtSlot()
    def getMechList(self):
        try:
            self.cur.execute("""SELECT ID, Name FROM MechanicView;""")
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            df.set_index('ID', inplace=True)
            self.parent.logSignal.emit("""SELECT ID, Name FROM MechanicView;""")
            return(df)
        except DatabaseError:
            print("Error Occured")
    
    @pyqtSlot()
    def getVList(self):
        try:
            self.cur.execute("""SELECT ID, Year, Make, Model FROM VehicleView;""")
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            df.set_index('ID', inplace=True)
            self.parent.logSignal.emit("""SELECT ID, Year, Make, Model FROM VehicleView;""")
            return(df)
        except DatabaseError:
            print("Error Occured")
    
    @pyqtSlot()
    def getMakeList(self):
        try:
            self.cur.execute("""SELECT Name, ID FROM Manufacturer;""")
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            df.set_index('ID', inplace=True)
            self.parent.logSignal.emit("""SELECT Name, ID FROM Make;""")
            return(df)
        except DatabaseError:
            print("Error Occured")

    @pyqtSlot(int, str)
    def softDelete(self, idx, table):
        try:
            self.cur.execute("""UPDATE `%s` SET isDeleted = 1 WHERE ID = %s;""" % (table,idx))
            self.parent.logSignal.emit("""UPDATE `%s` SET isDeleted = 1 WHERE ID = %s;""" % (table,idx))
            self.db.commit()
        except DatabaseError:
            print("Error Occured")

    def insertVehicle(self,row, mID, commit = True):
        try:
            self.cur.execute('''
                    INSERT INTO Vehicle(Year, Color, Miles, ModelID)
                    VALUES (%s,%s,%s,%s)
                    ''',
                        (row["Year"],
                        row["Color"],
                        row["Miles"],
                        mID)
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''INSERT INTO Vehicle(Year, Color, Miles, ModelID) VALUES (%s,%s,%s,%s)''' %
                        (row["Year"],
                        row["Color"],
                        row["Miles"],
                        mID)
                        )
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()

    def updateVehicle(self,row, mID, commit = True):
        try:
            self.cur.execute('''
                    UPDATE Vehicle
                    SET 
                        Year = %s, 
                        Color = %s, 
                        Miles = %s, 
                        ModelID = %s 
                    WHERE
                        ID = %s;
                    ''',
                        (row["Year"],
                        row["Color"],
                        row["Miles"],
                        mID,
                        row["ID"])
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit(''' UPDATE Vehicle SET Year = %s, Color = %s, Miles = %s, ModelID = %s WHERE ID = %s;''' %
                        (row["Year"],
                        row["Color"],
                        row["Miles"],
                        mID,
                        row["ID"]))
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()

    def filterVehicle(self, mID):
        try:
            self.cur.execute('SELECT * FROM VehicleView WHERE Make = %s', (mID,))
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            self.parent.viewSignal.emit(df)
            self.parent.logSignal.emit('SELECT * FROM VehicleView WHERE Make = %s' % (mID,))
        except DatabaseError:
            print("Error Occured")

    def insertMake(self,row, commit = True):
        try:
            self.cur.execute('''
                    INSERT INTO Manufacturer(Name)
                    VALUES (%s)
                    ''',
                        (row["Make"],)
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''INSERT INTO Manufacturer(Name) VALUES (%s)''' %
                        (row["Make"],)
                        )
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()

    def insertModel(self,row, mID, commit = True):
        try:
            self.cur.execute('''
                    INSERT INTO Model(Name, ManufacturerID)
                    VALUES (%s,%s)
                    ''',
                        (row["Model"],
                        mID)
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''INSERT INTO Model(Name, ManufacturerID) VALUES (%s,%s)
            ''' %
                        (row["Model"],
                        mID))
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()

    def insertInvoice(self,row, mID, vID, commit = True):
        try:
            self.cur.execute('''
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
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''INSERT INTO Invoice(Date, Amount, MechanicID, Description, Odometer, VehicleID) VALUES (%s,%s,%s,%s,%s,%s)''' %
                        (row["Date"],
                        row["Amount"],
                        mID,
                        row["Desc"],
                        row["Odo"],
                        vID))
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()
    
    def updateInvoice(self,row, mID, vID, commit = True):
        try:
            self.cur.execute('''
                    UPDATE Invoice
                    SET 
                        Date = %s, 
                        Amount = %s, 
                        MechanicID = %s, 
                        Description = %s, 
                        Odometer = %s, 
                        VehicleID = %s
                    WHERE
                        ID = %s;
                    ''',
                        (row["Date"],
                        row["Amount"],
                        mID,
                        row["Desc"],
                        row["Odo"],
                        vID,
                        row["ID"])
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''UPDATE Invoice SET Date = %s, Amount = %s, MechanicID = %s, Description = %s, Odometer = %s, VehicleID = %s WHERE ID = %s;''' %
                        (row["Date"],
                        row["Amount"],
                        mID,
                        row["Desc"],
                        row["Odo"],
                        vID,
                        row["ID"]))
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()

    def filterInvoice(self, mech, veh):
        try:
            if mech != -1 and veh != -1:
                self.cur.execute("""SELECT * FROM InvoiceView WHERE ID IN (
                    SELECT ID FROM Invoice WHERE MechanicID = %s AND VehicleID = %s
                );""" % (mech,veh))
                names = [des[0] for des in self.cur.description]
                myrecords = self.cur.fetchall()
                df = pd.DataFrame(myrecords, columns=names)
                self.parent.viewSignal.emit(df)
                self.parent.logSignal.emit("""SELECT ID FROM Invoice WHERE MechanicID IN (SELECT MechanicID FROM Invoice WHERE MechanicID = %s AND VehicleID = %s);""" % (mech,veh))
            elif mech != -1:
                self.cur.execute("""SELECT * FROM InvoiceView WHERE ID IN (
                    SELECT ID FROM Invoice WHERE MechanicID = %s);""" % (mech,))
                names = [des[0] for des in self.cur.description]
                myrecords = self.cur.fetchall()
                df = pd.DataFrame(myrecords, columns=names)
                self.parent.viewSignal.emit(df)
                self.parent.logSignal.emit("""SELECT * FROM InvoiceView WHERE ID IN (SELECT ID FROM Invoice WHERE MechanicID = %s);""" % (mech,))
            elif veh != -1:
                self.cur.execute("""SELECT * FROM InvoiceView WHERE ID IN (
                    SELECT ID FROM Invoice WHERE VehicleID = %s);""" % (veh,))
                names = [des[0] for des in self.cur.description]
                myrecords = self.cur.fetchall()
                df = pd.DataFrame(myrecords, columns=names)
                self.parent.viewSignal.emit(df)
                self.parent.logSignal.emit("""SELECT * FROM InvoiceView WHERE ID IN (SELECT ID FROM Invoice WHERE VehicleID = %s);""" % (veh,))
        except DatabaseError:
            print("Error Occured")

    def insertMechanic(self,row,commit = True):
        try:
            self.cur.execute('''
                    INSERT INTO Mechanic(Name, PhoneNumber, Address)
                    VALUES (%s,%s,%s)
                    ''',
                        (row["Name"],
                        row["Phone"],
                        row["Address"])
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''INSERT INTO Mechanic(Name, PhoneNumber, Address) VALUES (%s,%s,%s)''' %
                        (row["Name"],
                        row["Phone"],
                        row["Address"]))
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()
    
    def updateMechanic(self,row, commit = True):
        try:
            self.cur.execute('''
                    UPDATE Mechanic
                    SET 
                        Name = %s, 
                        PhoneNumber = %s, 
                        Address = %s
                    WHERE
                        ID = %s;
                    ''',
                        (row["Name"],
                        row["Phone"],
                        row["Address"],
                        row["ID"])
                        )
            if commit:
                self.db.commit()
            self.parent.logSignal.emit('''UPDATE Mechanic SET Name = %s, PhoneNumber = %s, Address = %s WHERE ID = %s;''' %
                        (row["Name"],
                        row["Phone"],
                        row["Address"],
                        row["ID"])
                        )
            return self.cur.lastrowid
        except DatabaseError:
            self.db.rollback()
    
    def filterMechanic(self, add):
        try:
            self.cur.execute('SELECT * FROM MechanicView WHERE Address LIKE %s', (add,))
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            df = pd.DataFrame(myrecords, columns=names)
            self.parent.viewSignal.emit(df)
            self.parent.logSignal.emit('SELECT * FROM MechanicView WHERE Address LIKE %s' % (add,))
        except DatabaseError:
            print("Error Occured")
    def checkExist(self,table, rowName, item):
        try:
            self.cur.execute(
                """SELECT ID FROM `%s` WHERE %s = '%s'""" %
                (table, rowName, item)
            )
            self.parent.logSignal.emit("""SELECT ID FROM `%s` WHERE %s = '%s'""" %
                (table, rowName, item))
            results = self.cur.fetchall()
            row_count = self.cur.rowcount
            if row_count == 0:
                return 0
            else:
                return results[0][0]
        except DatabaseError:
            print("Error Occured")

    def generateReports(self):
        try:
            self.cur.execute("""
                            SELECT V.Year, M2.Name AS Make, M3.Name AS Model, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
                            FROM
                                Invoice
                                    join Mechanic M on M.ID = Invoice.MechanicID
                                    join Vehicle V on V.ID = Invoice.VehicleID
                                    join Model M2 on V.ModelID = M2.ID
                                    join Manufacturer M3 on M3.ID = M2.ManufacturerID
                            WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
                            GROUP BY V.ID;
                            """)
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            pd.DataFrame(myrecords, columns=names).to_csv("Vehicle_Summary.csv",encoding='utf-8', index=False)
            self.cur.execute("""
                            SELECT M.Name AS Mechanic, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
                            FROM
                                Invoice
                                    join Mechanic M on M.ID = Invoice.MechanicID
                                    join Vehicle V on V.ID = Invoice.VehicleID
                                    join Model M2 on V.ModelID = M2.ID
                                    join Manufacturer M3 on M3.ID = M2.ManufacturerID
                            WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
                            GROUP BY M.ID;
                            """)
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            pd.DataFrame(myrecords, columns=names).to_csv("Mechanic_Summary.csv",encoding='utf-8', index=False)
            self.cur.execute("""
                            SELECT M3.Name AS Manufactuer, AVG(Amount) AS "Average Invoice Amount", SUM(Amount) as "Total Invoice Amount"
                            FROM
                                Invoice
                                    join Mechanic M on M.ID = Invoice.MechanicID
                                    join Vehicle V on V.ID = Invoice.VehicleID
                                    join Model M2 on V.ModelID = M2.ID
                                    join Manufacturer M3 on M3.ID = M2.ManufacturerID
                            WHERE Invoice.isDeleted != 1 AND V.isDeleted !=1 and M.isDeleted != 1
                            GROUP BY M3.ID;
                            """)
            names = [des[0] for des in self.cur.description]
            myrecords = self.cur.fetchall()
            pd.DataFrame(myrecords, columns=names).to_csv("Manufactuer_Summary.csv",encoding='utf-8', index=False)
            return(True)
        except DatabaseError:
            print("Error Occured")





