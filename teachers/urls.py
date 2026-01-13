from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('add/', views.add_teacher, name='add_teacher'),
    path('list/', views.teacher_list, name='teacher_list'),

    path('take-attendance', views.take_attendance, name='attandence'),

    path('add-marks/', views.add_marks, name='add_marks'),
    path('add-exams/', views.add_exams, name='add_exams'),


]
