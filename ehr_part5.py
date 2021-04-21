'''ehr part5'''
import sqlite3
from time import sleep
import uuid
import urllib.request

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional

APP = FastAPI()


con = sqlite3.connect("biostat821.db")

cur = con.cursor()

# create table
cmd_patients = """
CREATE TABLE if not exists patients 
(PatientID text, PatientGender text, PatientDateOfBirth text, PatientRace text, 
PatientMaritalStatus text, PatientLanguage text, PatientPopulationPercentageBelowPoverty text)
"""


#create table
cmd_table = """
CREATE TABLE if not exists labs 
(PatientID text, AdmissionID text, LabName text, LabValue text, 
LabUnits text, LabDateTime text)
"""

cur.execute(cmd_patients)
cur.execute(cmd_table)


sql_insert = "INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?)"
for line in urllib.request.urlopen('http://biostat821.colab.duke.edu/patients.txt'):
    line = line.decode()
    line = line.replace('\n','').split('\t')
    cur.execute(sql_insert, (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))


sql_insert = "INSERT INTO labs VALUES (?, ?, ?, ?, ?, ?)"
for line in urllib.request.urlopen("http://biostat821.colab.duke.edu/labs.txt"):
    line = line.decode()
    line = line.replace('\n','').split('\t')
    cur.execute(sql_insert, (line[0], line[1], line[2], line[3], line[4], line[5]))


con.commit()

'''Define URL class'''
class URL(BaseModel):
    url: str

class Sick(BaseModel):
    lab_name: str
    lab_value: float

@APP.get("/patients/{id}")
def ThePerson(id: str):
    """Get person by id"""
    con = sqlite3.connect("biostat821.db")
    cur = con.cursor()
    cmd = f"SELECT * from patients where Patientid='{id}'"
    cur.execute(cmd)
    results = cur.fetchone()
    if results is None:
        raise HTTPException(404, "No person")
    con.close()
    results={"Patientid":results[0],
    "PatientGender":results[1],
    "PatientDateOfBirth":results[2],
    "PatientRace":results[3],
    "PatientMaritalStatus":results[4],
    "PatientLanguage":results[5]}
    con.close()
    return results

@APP.get("/patients/{id}/labs")
def TheLab(id:str):
    """Get person lab data by id"""
    con = sqlite3.connect("biostat821.db")
    cur = con.cursor()
    cmd = f"SELECT * from labs where Patientid='{id}'"
    cur.execute(cmd)
    table = []
    for line in cur.fetchall():
        table.append({"admission_id":line[1],
        "name":line[2],
        "value":line[3],
        "units":line[4],
        "datetime":line[5]})
    con.close()
    return table

@APP.get("/num_older_than")
def num_older_than(age: float) -> int:
    try:
        float(age)
    except ValueError:
        print("'age' needs to be a number")
        return False
    num = 0
    con = sqlite3.connect("biostat821.db")
    cur = con.cursor()
    cmd = "SELECT PatientDateOfBirth from patients"
    cur.execute(cmd)
    now_year = datetime.now().year
    now_month = datetime.now().month
    for line in cur.fetchall()[1:]:
        line = datetime.strptime(line[0],'%Y-%m-%d %H:%M:%S.%f')
        p_year = line.year
        p_month = line.month
        gap = (now_year-p_year)+(now_month-p_month)/12
        if gap > age:
           num += 1
    con.close()
    return num


@APP.get("/sick_patients")
def SickPatients(lab_name: str, operator: str, lab_value: float):
    if operator == "<" or operator == ">":
        pass
    else:
        print("'operator' should be '>' or '<' in string")
        return False
    con = sqlite3.connect("biostat821.db")
    cur =con.cursor()
    cmd = f"SELECT PatientID, LabValue from labs WHERE LabName='{lab_name}'"
    cur.execute(cmd)
    List = []
    for line in cur.fetchall():
        if (operator=='<'): 
            if line[1]<lab_value:
                List.append(line[0])
        else:
            if line[1]>lab_value:
                List.append(line[0])
    con.close()
    return list(set(List))

'''Post functions'''
@APP.post("/labs")
def LabsPlus(link:URL):
    with urllib.request.urlopen(link.url) as response:
        lab_data=[]
        for line in response:
            line = line.decode('utf-8')
            row = line.strip('\r\n').replace('\t',',')
            item = row.split(',')
            lab_data.append(item)
    con = sqlite3.connect("biostat821.db")
    cur = con.cursor()
    cur.executemany('INSERT INTO labs VALUES (?, ?, ?, ?, ?, ?)', lab_data)
    con.commit()
    con.close()
    return "Succeed load lab data"



@APP.post("/patients")
def PatientsPlus(link:URL):
    with urllib.request.urlopen(link.url) as response:
        patient_data = []
        for line in response:
            line=line.decode('utf-8')
            row=line.strip('\r\n').replace('\t',',')
            item=row.split(',')
            patient_data.append(item)
    con = sqlite3.connect("biostat821.db")
    cur = con.cursor()
    cur.executemany('INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?)', patient_data)
    con.commit()
    con.close()
    return "Succeed load patient data"


