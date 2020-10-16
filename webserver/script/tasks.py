from celery import shared_task, current_task
from script.CostBenefitAnalysis.preprocessing_loadprofiles.split_file import split_file
from script.CostBenefitAnalysis.UploadToPostgres import UploadToPostgres
from celery.execute import send_task

#for running CBA tool
import sys
sys.path.append("script/CostBenefitAnalysis/python_code/")
from model_class import ModelInstance

@shared_task
def run_cba_tool(county_data, profile_name):
    split_file(county = county_data)
    ModelInstance()
    UploadToPostgres(load_profile = profile_name)
    return
