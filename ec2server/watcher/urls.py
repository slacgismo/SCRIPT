from django.urls import path, re_path, include

import watcher.views

urlpatterns = [
    path('refresh', watcher.views.progress_view, name='refresh'),
]
