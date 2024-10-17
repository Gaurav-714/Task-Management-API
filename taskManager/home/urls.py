from django.urls import path
from .views import *

urlpatterns = [
    path('', CreateListTaskView.as_view()),
]
