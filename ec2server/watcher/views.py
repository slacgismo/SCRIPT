from django.shortcuts import render
from django.http import JsonResponse

from watcher.tasks import my_task

# Create your views here.

def progress_view(request):
    result = my_task.delay(10)
    return JsonResponse({'task_id': result.id})
