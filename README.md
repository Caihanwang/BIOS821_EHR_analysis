# ehr_analysis by Caihan

## setup/installation instructions, including information about the expected input file formats
* load_patients and load_labs
    You should input name of txt document and it will output lists of data table 
* num_older_than
    You should input a data table containing a list named 'PatientDateOfBirth' and a parameter, it will output the number of people whose age larger than the parameter.
* sick_patients
    You should input a data table containing lists named 'LabName','LabValue' and '\ufeffPatientID', it will output the ID of patients.
* age_first_admission
    You should input two data table and 1 patient ID, it will output this patient age when first admission.


## examples
```python
>> patients = load_patients("PatientCorePopulatedTable.txt")
>> print(num_older_than(patients,51.2))
75
```

```python
>> labels = load_labs("LabsCorePopulatedTable.txt")
>> print(len(sick_patients(labels, "METABOLIC: ALBUMIN", ">",4.0)))
100
```

```python
>> patients = load_patients("PatientCorePopulatedTable.txt")
>> labels = load_labs("LabsCorePopulatedTable.txt")
>> print(age_first_admission(patients, labels, '1A8791E3-A61C-455A-8DEE-763EB90C9B2C'))
18
```
