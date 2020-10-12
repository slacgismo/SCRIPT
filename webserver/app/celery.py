import os
from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.base')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings.base')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

  
# import os
# from celery import Celery


# broker_url = os.getenv('CELERY_BROKER_URL', 'filesystem://')
# broker_dir = os.getenv('CELERY_BROKER_FOLDER', './broker')

# for f in ['out', 'processed']:
#     if not os.path.exists(os.path.join(broker_dir, f)):
#         os.makedirs(os.path.join(broker_dir, f))


# app = Celery(__name__)
# app.conf.update({
#     'broker_url': broker_url,
#     'broker_transport_options': {
#         'data_folder_in': os.path.join(broker_dir, 'out'),
#         'data_folder_out': os.path.join(broker_dir, 'out'),
#         'data_folder_processed': os.path.join(broker_dir, 'processed')
#     },
#     'imports': ('tasks',),
#     'result_persistent': False,
#     'task_serializer': 'json',
#     'result_serializer': 'json',
#     'accept_content': ['json']})