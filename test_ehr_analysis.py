from datetime import datetime
from ehr_analysis import num_older_than, patients, sick_patients, labels, load_patients, load_labs, age_first_admission


def test_num_older_than():
    """Test num_older_than()."""
    patients = {
        'PatientDateOfBirth': ['2021-01-01 00:00:00.00', '1920-01-01 00:00:00.00', '1920-01-01 00:00:00.00']
    }
    assert num_older_than(patients, 50) == 2

def test_sick_patients():
    """Test sick_patients()"""
    labels = {
        'LabName': ["URINALYSIS: PH", "URINALYSIS: PH", ""],
        'LabValue': ['10.3', '3.0', '8.7'],
        '\ufeffPatientID': ["Paul", "Anderson", "John"]
    }
    result = sick_patients(labels, "URINALYSIS: PH", ">", 5.0)
    assert len(result) == 1
    assert result[0] == "Paul"

def test_sick_patients_duplicate():
    """Test duplicates in sick_patients()."""
    labels ={
        'LabName': ["URINALYSIS: PH", "URINALYSIS: PH", "URINALYSIS: PH"],
        'LabValue': ['10.3', '11.5', '8.7'],
        '\ufeffPatientID': ["Paul", "Paul", "John"]
    }
    result = sick_patients(labels, "URINALYSIS: PH", ">", 10.0)
    assert len(result) == 1
    assert result[0] == "Paul"

def test_load_patients():
    """Test load_patients()."""
    result = load_patients("PatientCorePopulatedTable.txt")
    assert len(result) == 7

def test_load_labs():
    """Test load_labs()."""
    result = load_labs("LabsCorePopulatedTable.txt")
    assert len(result) == 6

def test_age_first_admission():
    """Test age_first_admission"""
    patients = {
        '\ufeffPatientID': ['Paul','John','Anderson'],
        'PatientDateOfBirth': ['1972-01-01 00:00:00.00', '1983-01-01 00:00:00.00', '1994-01-01 00:00:00.00']
    }
    labels= {
        '\ufeffPatientID': ['Paul','Paul','Amy','Jack'],
        'LabDateTime': ['2020-01-01 00:00:00.00\n', '2018-01-01 00:00:00.00\n', '2016-01-01 00:00:00.00\n','']
    }
    result = age_first_admission(patients,labels,'Paul')
    assert result == 46