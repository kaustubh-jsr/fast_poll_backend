from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('create_poll',create_poll),
    path('get_poll',get_poll),
    path('caste_vote',caste_vote),
]