from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name="login"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('add_user/', add_user, name="add_user"),
]