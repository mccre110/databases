# https://datatofish.com/import-csv-sql-server-python/
# https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm
# https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
import sqlite3
import pandas as pd

conn = sqlite3.connect('./StudentDB.db')
cur = conn.cursor()


class Student:
    def __init__(self, FirstName, LastName, GPA, Major, FacultyAdvisor, Address,  City, State, ZipCode, MobilePhoneNumber):
        self.FirstName = FirstName
        self.LastName = LastName
        self.GPA = GPA
        self.Major = Major
        self.Address = Address
        self.FacultyAdvisor = FacultyAdvisor
        self.City = City
        self.State = State
        self.ZipCode = ZipCode
        self.MobilePhoneNumber = MobilePhoneNumber

    def check(self):
        if not self.FirstName.isalpha():
            return False
        if not self.LastName.isalpha():
            return False
        if not self.GPA.isdecimal():
            return False
        if self.Address.isdigit():
            return False
        if not self.ZipCode.isnumeric():
            return False
        if self.MobilePhoneNumber.isalpha():
            return False
        return True


def importCSV():
    data = pd.read_csv('./students.csv')
    for row in data.itertuples():
        cur.execute('''
        INSERT INTO Student(FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ''',
                    (row.FirstName,
                     row.LastName,
                     row.GPA,
                     row.Major,
                     row.Address,
                     row.City,
                     row.State,
                     row.ZipCode,
                     row.MobilePhoneNumber,
                     0)
                    )
    conn.commit()


def displayAll():
    cur.execute('select * from Student;')
    names = [des[0] for des in cur.description]
    myrecords = cur.fetchall()
    df = pd.DataFrame(myrecords, columns=names)
    print(df.to_string())


def getInputS():
    uFirstName =input("Enter First Name:")
    uLastName =input("Enter Last Name:")
    uGPA =input("Enter GPA:")
    uMajor =input("Enter Major:")
    uFac = input("Enter Faculty Advisor:")
    uAddress =input("Enter Address:")
    uCity =input("Enter City:")
    uState =input("Enter State:")
    uZipCode =input("Enter Zipcode:")
    uMobilePhoneNumber =input("Enter Mobile Phone:")
    s = Student(uFirstName, uLastName, uGPA, uMajor, uFac, uAddress, uCity, uState, uZipCode, uMobilePhoneNumber,)
    if s.check():
        return s
    else:
        print("Invalid entry")
        return None


def addStudent(student):
    if student:
        cur.execute('''
                    INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?);
                    ''',
                    (student.FirstName,
                     student.LastName,
                     student.GPA,
                     student.Major,
                     student.FacultyAdvisor,
                     student.Address,
                     student.City,
                     student.State,
                     student.ZipCode,
                     student.MobilePhoneNumber,
                     0)
                    )
        conn.commit()


def getInputSID():
    sid = input("Enter Student ID:")
    if sid.isnumeric():
        cur.execute('Select * from Student where StudentId = ?', (sid,))
        conn.commit()
        x = cur.fetchall()
        if len(x) > 0:
            return sid
    else:
        print("Bad ID")
        return None


def updateS(sid):
    if sid:
        uinput = input("""
        1. Major
        2. Advisor
        3. Phone Number
        """)
        if uinput == "1":
            nmajor = input("New Major: ")
            cur.execute('Update Student set Major = ? where StudentId = ?', (nmajor, sid))
            conn.commit()
        elif uinput == "2":
            nadvisor = input("New Advisor: ")
            cur.execute('Update Student set FacultyAdvisor = ? where StudentId = ?', (nadvisor, sid))
            conn.commit()

        elif uinput == "3":
            nphone = input("New Phone: ")
            cur.execute('Update Student set MobilePhoneNumber = ? where StudentId = ?', (nphone, sid))
            conn.commit()


def deleteS(sid):
    if sid:
        cur.execute('Update Student set isDeleted = 1 where StudentId = ?', (sid,))
        conn.commit()


def search():
    uinput = input("""
1. Major
2. GPA
3. City
4. State
5. Advisor
    """)
    if uinput == "1":
        nmajor = input("Major: ")
        cur.execute('select * from Student where Major = ?',(nmajor,))
        names = [des[0] for des in cur.description]
        myrecords = cur.fetchall()
        df = pd.DataFrame(myrecords, columns=names)
        print(df.to_string())

    elif uinput == "2":
        nGPA = input("GPA: ")
        cur.execute('select * from Student where GPA = ?',(nGPA,))
        names = [des[0] for des in cur.description]
        myrecords = cur.fetchall()
        df = pd.DataFrame(myrecords, columns=names)
        print(df.to_string())

    elif uinput == "3":
        nCity = input("City: ")
        cur.execute('select * from Student where City = ?', (nCity,))
        names = [des[0] for des in cur.description]
        myrecords = cur.fetchall()
        df = pd.DataFrame(myrecords, columns=names)
        print(df.to_string())

    elif uinput == "4":
        nstate = input("State: ")
        cur.execute('select * from Student where State =?', (nstate,))
        names = [des[0] for des in cur.description]
        myrecords = cur.fetchall()
        df = pd.DataFrame(myrecords, columns=names)
        print(df.to_string())

    elif uinput == "5":
        nadv = input("Advisor: ")
        cur.execute('select * from Student where FacultyAdvisor =?', (nadv,))
        names = [des[0] for des in cur.description]
        myrecords = cur.fetchall()
        df = pd.DataFrame(myrecords, columns=names)
        print(df.to_string())


if __name__ == "__main__":
    while True:
        print("""
1. Display All
2. Add a student
3. Update a student
4. Delete a student
5. Search
6. Quit
        """)
        uinput = input("")
        if uinput == "1":
            displayAll()
        elif uinput == "2":
            addStudent(getInputS())
        elif uinput == "3":
            updateS(getInputSID())
        elif uinput == "4":
            deleteS(getInputSID())
        elif uinput == "5":
            search()
        elif uinput == "6":
            break
        else:
            continue
