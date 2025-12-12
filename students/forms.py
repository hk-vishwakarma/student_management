from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name", "student_class", "roll_no",
            "dob", "address", "photo"
        ]
