# import packages
from datetime import datetime
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np



class Patient:
    '''Patient Function'''

    def __init__(self, ID):
        '''initilized'''
        # read in data
        patients = pd.read_table('PatientCorePopulatedTable.txt', sep = '\t')
        self.ID = ID
        the_patient = patients[patients['PatientID']== self.ID]
        self.gender = list(the_patient['PatientGender'])[0]
        self.DOB = list(the_patient['PatientDateOfBirth'])[0]
        self.race = list(the_patient['PatientRace'])[0]
        self.marital_status = list(the_patient['PatientMaritalStatus'])[0]
        self.language = list(the_patient['PatientLanguage'])[0]
        self.poverty = list(the_patient['PatientPopulationPercentageBelowPoverty'])[0]
        # calculate patients' age
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        currentdate = datetime.today()
        birthdate = datetime.strptime(self.DOB, date_format)
        delta = currentdate-birthdate
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
        # read in data
        Labs = pd.read_table('LabsCorePopulatedTable.txt', sep = '\t')
        # filter Labs1 with ID and labname
        Labs1 = Labs[Labs['PatientID']== self.ID]
        Labs1 = Labs1[Labs1['LabName']==labname]
        # convert date format
        Labs1['LabDateTime']=pd.to_datetime(Labs1['LabDateTime'])
        # sort with time
        Labs1.sort_values('LabDateTime',inplace=True)
        # plot
        plt.clf()
        plt.scatter(Labs1['LabDateTime'], Labs1['LabValue'])
        plt.xticks(rotation = 45)
        plt.xlabel('Time')
        plt.ylabel(f"Lab Value ({list(Labs1['LabUnits'])[0]})")
        plt.title(f"Patient ID: {self.ID} \n in {labname}")
        plt.tight_layout()
        plt.savefig(filename)

            

    
class Observation:
    '''observation'''
    def __init__(self, ID, labname, value, units, time):
        self.ID = ID
        self.labname = labname
        self.value = value
        self.units = units
        self.time = time



