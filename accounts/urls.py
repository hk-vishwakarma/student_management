from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name="login"),
    path('add_user/', add_user, name="add_user"),
]