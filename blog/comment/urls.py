from django.urls import path
from .views import *


urlpatterns = [
    path('comment/', CommentView.as_view(), name='comment'),
]