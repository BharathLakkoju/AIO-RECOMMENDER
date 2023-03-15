from django.urls import path
from temp.views import *

urlpatterns = [
    path('', index.as_view(), name='temp'),
    path('recommend/', recommend.as_view(), name='recommendations'),
]