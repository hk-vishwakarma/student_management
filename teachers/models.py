from django.db import models
from django.conf import settings
from students.models import Student
from academics.models import SchoolClass, Subject

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    date_joined = models.DateField()

    def __str__(self):
        return self.full_name


class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)

    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_name} - {self.subject} - {self.date}"


class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='records'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    status = models.BooleanField(default=False)  # True = Present

    def __str__(self):
        return f"{self.student.user.username} - {'Present' if self.status else 'Absent'}"
