# EHR Analysis Part 3
## setup/installation instructions
Requirement: 
1. numpy = 1.20.1
2. matplotlib = 3.3.4
3. pandas = 1.2.2
4. Data sets of LabsCorePopulatedTable.txt and PatientCorePopulatedTable.txt should be put into the same folder with the ehr_analysis_p3.py

Input File Format:  
1. Patient's ID should be input to the function. After that call 'Patient().age' could output the patient's age. And it also can compare the age with other patient or a float. 
2. For plot function, lab name and file name should be input, sucha as 'Patient().plot('labname','filename') and it will create a figure of time and lab value about the patient.

## Examples
1. 
```python
a = Patient('1A8791E3-A61C-455A-8DEE-763EB90C9B2C')
b = Patient('64182B95-EB72-4E2B-BE77-8050B71498CE')

print(a>b)
print(a.gender)
print(a > 75.0)
print(a.age)

```
output:  
The first patient is not older than the second patient  
Male  
The age of patient is not larger than 75.0  
48  

2. 
```python
a.plot('METABOLIC: GLUCOSE','glucose_over_time.png')

```

## Testing Instruction
In the test function, we use two examples of two patients and name them as a and b. We test for a>b, a>75.0, a.gender, a.age and so on. 