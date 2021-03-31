# import packages
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

con = sqlite3.connect(":memory:")

cur = con.cursor()


'''Read patient data into sql database'''
# create table
cmd = """
CREATE TABLE patients 
(PatientID text, PatientGender text, PatientDateOfBirth text, PatientRace text, 
PatientMaritalStatus text, PatientLanguage text, PatientPopulationPercentageBelowPoverty text)
"""
cur.execute(cmd)

sql_insert = "INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?)"
with open('PatientCorePopulatedTable.txt') as patients:
    for line in patients.readlines():
        line = line.replace('\n','').split('\t')
        cur.execute(sql_insert, (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))



'''Read labs data into sql database'''
#create table
cmd = """
CREATE TABLE labs 
(PatientID text, AdmissionID text, LabName text, LabValue text, 
LabUnits text, LabDateTime text)
"""
cur.execute(cmd)

sql_insert = "INSERT INTO labs VALUES (?, ?, ?, ?, ?, ?)"
with open('LabsCorePopulatedTable.txt') as labs:
    for line in labs.readlines():
        line = line.replace('\n','').split('\t')
        cur.execute(sql_insert, (line[0], line[1], line[2], line[3], line[4], line[5]))



class Patient:
    '''Patient Function'''

    def __init__(self, cursor, ID):
        '''initilized'''
        self.cursor = cursor
        self.ID = ID
        # fetch patient's DOB
        query = f"SELECT patients.PatientDateOfBirth FROM patients WHERE patients.PatientID = '{self.ID}'"
        cursor.execute(query)
        self.DOB = cursor.fetchall()
        # calculate patients' age
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        currentdate = datetime.today()
        birthdate = datetime.strptime(self.DOB[0][0], date_format)
        delta = currentdate - birthdate
        self._age = round(delta.days/365)

    @property
    def age(self):
        return self._age   



    def __lt__(self, other):
        '''less than function'''
        if type(other)==float:
            if self.age < other:
                return f"The age of patient is less than {other}"
            else:
                return f"The age of patient is not less than {other}"
        else:
            if self.age < other.age:
                return "The first patient is younger than the second patient"
            else:
                return "The first patient is not younger than the second patient"

    def __gt__(self, other):
        '''greater than function'''
        if type(other)==float:
            if self.age > other:
                return f"The age of patient is larger than {other}"
            else:
                return f"The age of patient is not larger than {other}"                
        else:
            if self.age > other.age:
                return "The first patient is older than the second patient"
            else:
                return "The first patient is not older than the second patient" 


    def plot(self, labname, filename):
        '''plot function'''

        # filter Labs with ID and labname
        query = f'''
        SELECT labs.LabValue, labs.LabUnits, labs.LabDateTime FROM labs 
        WHERE labs.PatientID = '{self.ID}' AND labs.LabName = '{labname}'
        '''
        self.cursor.execute(query)
        The_Lab = self.cursor.fetchall()

        # convert list to dataframe
        The_Lab = pd.DataFrame(The_Lab)

        # convert date format
        The_Lab[2]=pd.to_datetime(The_Lab[2])

        # sort with time
        The_Lab.sort_values(2,inplace=True)

        # plot
        plt.clf()
        plt.scatter(The_Lab[2], pd.to_numeric(The_Lab[0]))
        plt.xticks(rotation = 45)
        plt.xlabel('Time')
        plt.ylabel(f"Lab Value ({list(The_Lab[1])[0]})")
        plt.title(f"Patient ID: {self.ID} \n in {labname}")
        plt.tight_layout()
        plt.savefig(filename)


con.commit()





