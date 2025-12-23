from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import StudentForm
from .models import Student
from django.core.paginator import Paginator
from accounts.models import User

def add_student(request):

    if request.method == "POST":

        # LOGIN DETAILS (LEFT SIDE)
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # STUDENT DETAILS (RIGHT SIDE)
        student_form = StudentForm(request.POST, request.FILES)

        if student_form.is_valid():

            # Create User
            user = User.objects.create_user(
                username=username,
                password=password,
                role='student'
            )

            # Create Student
            student = student_form.save(commit=False)
            student.user = user
            student.phone = phone
            student.role = "student"
            student.save()

            return redirect("student_list")

    return render(request, "students/add_student.html")


# list all students or search students
def student_list(request):
    
    q = request.GET.get('q', '')

    students = Student.objects.filter(full_name__icontains=q).order_by('id')

    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students_page = paginator.get_page(page)

    return render(request, 'students/students_list.html', {
        'students': students_page
    })
    
