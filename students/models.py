from django.db import models
from django.conf import settings
from academics.models import SchoolClass
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to="students_profile/", blank=True)

    phone = models.CharField(max_length=20, blank=True)  
    role = models.CharField(max_length=20, default="student")

    def __str__(self):
        return self.full_name
