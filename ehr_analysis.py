import datetime


def load_patients(filename):
    labels_table = []
    data_table = {}
    with open(filename) as stream:
        stream_lines = stream.readlines()
        labels_table = stream_lines[0].split()
        for label in labels_table:
            data_table[label]=[]
        for line in stream_lines[1:]:
            line_data = line.split('\t')
            for i in range(len(labels_table)):
                data_table[labels_table[i]].append(line_data[i])
    return data_table



def num_older_than(patients,age):
    date = []
    date = patients['PatientDateOfBirth']
    index=0
    from datetime import datetime
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    currentdate = datetime.strptime('2021-2-10 00:00:00.000', date_format)
    for i in range(len(date)):
        birthdate = datetime.strptime(date[i], date_format)
        delta = currentdate-birthdate
        if delta.days/365>age:
            index=index+1
    return index

patients = load_patients("PatientCorePopulatedTable.txt")
print(num_older_than(patients,51.2))

def load_labs(filename):
    labels = {}
    data= []
    with open(filename) as stream:
        stream_lines = stream.readlines()
        data = stream_lines[0].split()
        for i in data:
            labels[i] = []
        for j in stream_lines[1:]:
            line_data = j.split('\t')
            for k in range(len(data)):
                labels[data[k]].append(line_data[k])
    return labels




def sick_patients(labels, lab, gt_lt, value):
    if not gt_lt in ['>','<']:
        raise ValueError(f"{gt_lt} should be > or <")
    if not isinstance(value,(int,float)):
        raise ValueError(f"{value} should be int or float")
    LabName = labels['LabName']
    LabValue = labels['LabValue']
    PatientID = labels['\ufeffPatientID']
    Name=[]
    if gt_lt == ">":
        for i,name in enumerate(LabName):
            if name == lab and float(LabValue[i])>value:
                Name.append(PatientID[i])
    if gt_lt == "<":
        for i,name in enumerate(LabName):
            if name == lab and float(LabValue[i])<value:
                Name.append(PatientID[i])
    return list(set(Name))


labels = load_labs("LabsCorePopulatedTable.txt")
print(sick_patients(labels, "METABOLIC: ALBUMIN", ">",4.0))

def age_first_admission(patients, labels, ID):
    from datetime import datetime
    date_format = '%Y-%m-%d %H:%M:%S.%f'
   
    
    for i in range(len(patients['PatientDateOfBirth'])):
        if patients['\ufeffPatientID'][i] == ID:
            Birthday = patients['PatientDateOfBirth'][i]
    Birthday = datetime.strptime(Birthday, date_format)        
    

    LabDateTime=[]
    for j in range(len(labels['LabDateTime'])):
        if labels['\ufeffPatientID'][j] == ID:
            LabDateTime.append(labels['LabDateTime'][j])
    
    age=[]
    for k in range(len(LabDateTime)):
        Time = datetime.strptime(LabDateTime[k], '%Y-%m-%d %H:%M:%S.%f\n')
        delta = Time - Birthday
        age.append(int(delta.days/365))

    age=min(age)
    return(age)

print(age_first_admission(patients, labels, '1A8791E3-A61C-455A-8DEE-763EB90C9B2C'))
    




