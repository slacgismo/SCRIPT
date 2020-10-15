from celery import shared_task, current_task
from script.CostBenefitAnalysis.preprocessing_loadprofiles.split_file import split_file
from script.CostBenefitAnalysis.UploadToPostgres import UploadToPostgres
#for running CBA tool
import sys
sys.path.append("script/CostBenefitAnalysis/python_code/")
from model_class import ModelInstance

@shared_task
def split_file(county_data, profile_name):
    split_file(county = county_data)
    return

@shared_task
def run_cba_tool():
    ModelInstance()
    return

@shared_task
def upload_to_db(profile_name):
    UploadToPostgres(load_profile = profile_name)
    return