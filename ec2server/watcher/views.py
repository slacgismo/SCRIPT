from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def progress_view(request):
    return JsonResponse({'task_id': 1})
