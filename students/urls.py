from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path("add/", views.add_student, name="add_student"),
    path("list/", views.student_list, name="student_list"),
]
