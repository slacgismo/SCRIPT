import string
import time

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def my_task(total):
    for i in range(total):
        print(i)
        time.sleep(1)
    return '{} success!'.format(total)
