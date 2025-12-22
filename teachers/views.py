from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Teacher
from django.http import HttpResponseForbidden
from datetime import date

from .models import Attendance, AttendanceRecord
from students.models import Student
from django.contrib import messages

# Create your views here.

# add teachers
def add_teacher(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        full_name = request.POST['full_name']
        subject = request.POST['subject']
        phone = request.POST['phone']
        address = request.POST['address']
        date_joined = request.POST['date_joined']
        profile_pic = request.FILES.get('profile_pic')

        # Create user
        user = User.objects.create_user(username=username, password=password, role='teacher')
        user.save()

        # Create teacher profile
        Teacher.objects.create(
            user=user,
            full_name=full_name,
            subject=subject,
            phone=phone,
            address=address,
            date_joined=date_joined,
            profile_pic=profile_pic
        )

        return redirect('teachers:teacher_list')

    return render(request, 'teachers/add_teacher.html')

# list all teachers
def teacher_list(request):
    teachers = Teacher.objects.all().order_by('id')
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})


def take_attendance(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("Access Denied")

    students = None

    # Load students
    if request.method == 'GET' and 'class_name' in request.GET:
        class_name = request.GET.get('class_name')
        students = Student.objects.filter(student_class=class_name)

        if not students.exists():
            messages.warning(request, "No students found for selected class.")

    # Save attendance
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        today = date.today()

        attendance, created = Attendance.objects.get_or_create(
            class_name=class_name,
            subject=subject,
            teacher=request.user,
            date=today
        )

        if not created:
            messages.error(request, "Attendance already taken for today!")
            return redirect('teachers:attendance')

        students = Student.objects.filter(student_class=class_name)

        for student in students:
            status_value = request.POST.get(f'attendance_{student.id}')

            AttendanceRecord.objects.create(
                attendance=attendance,
                student=student,
                status=True if status_value == 'Present' else False
            )

        messages.success(request, "Attendance saved successfully!")
        return redirect('teachers:attendance')

    return render(request, 'teachers/attendance.html', {'students': students})