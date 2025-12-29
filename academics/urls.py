from django.urls import path
from .views import *

app_name = 'academics'

urlpatterns = [
    path('classes/', class_list, name='class_list'),
    path('subjects/', manage_subjects, name='manage_subjects'),


]