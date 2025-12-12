from django.db import models
from django.conf import settings

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
