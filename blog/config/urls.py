from django.urls import path
from .views import *


urlpatterns = [
    path('links/', LinkListView.as_view(), name='links'),
]