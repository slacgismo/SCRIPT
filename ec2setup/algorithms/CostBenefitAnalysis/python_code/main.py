from __future__ import unicode_literals
import os
import model_class
import pandas as pd

cases_to_run = os.getcwd().replace('\python_code', '\Cases to run.csv')
case_list = pd.read_csv(cases_to_run)['Case Name'].to_list()
case_number = 1
for case in case_list:
    print("Running Case {} of {} - Case Name: '{}'".format(case_number, len(case_list), case))
    model = model_class.ModelInstance(case)
    case_number += 1