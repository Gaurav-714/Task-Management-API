from django.urls import path
from .views import *

urlpatterns = [
    path('', CreateListTaskView.as_view()),
    path('<uuid:task_id>/', UpdateRetrieveTaskView.as_view()),
]
