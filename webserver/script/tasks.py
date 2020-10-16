from celery import shared_task, current_task
from script.CostBenefitAnalysis.preprocessing_loadprofiles.split_file import split_file
from script.CostBenefitAnalysis.UploadToPostgres import UploadToPostgres
from celery.execute import send_task
import sys
# sys.path.append("../app/settings/")
# from celery import app

#for running CBA tool
sys.path.append("script/CostBenefitAnalysis/python_code/")
from model_class import ModelInstance

@shared_task
def run_cba_tool(county_data, profile_name):
    split_file(county = county_data)
    ModelInstance()
    UploadToPostgres(load_profile = profile_name)
    return

@shared_task
def check_task_status(task_name):
    ''' checks celery if algorithm runner status is completed '''
    task = send_task(task_name)
    return task.state