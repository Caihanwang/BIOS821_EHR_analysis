# import packages
from datetime import datetime
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from ehr_analysis_p4 import Patient
from ehr_analysis_p4 import cur
import sqlite3


def test_Patient():
    ''' test patient '''
    a = Patient(cur, '1A8791E3-A61C-455A-8DEE-763EB90C9B2C')
    b = Patient(cur, '64182B95-EB72-4E2B-BE77-8050B71498CE')
    result1 = a>b
    result2 = a > 75.0
    assert result1 == 'The first patient is not older than the second patient'
    assert result2 == 'The age of patient is not larger than 75.0'
    assert a.gender == 'Male'
    assert a.age == 48
    assert a.DOB == '1973-08-16 10:58:34.413'
    assert a.race == 'Asian'
    assert a.marital_status == 'Single'
    assert a.language == 'English'
    assert a.poverty == 13.97