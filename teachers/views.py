from django.shortcuts import render, redirect
from django.conf import settings
from .models import Teacher, Exam, Marks
from django.http import HttpResponseForbidden
from datetime import date
from accounts.models import User

from .models import Attendance, AttendanceRecord
from students.models import Student
from academics.models import SchoolClass, Subject
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

        new_user = User.objects.filter(username = username)
        if new_user.exists():
            messages.error(request, "Username already exists !")
            return redirect('teachers:add_teacher')

        # Create user
        user = User.objects.create_user(
            full_name=full_name,
            username=username,
            password=password, 
            role='teacher'
        )
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
    classes = SchoolClass.objects.all()
    students = None
    subjects = None
    selected_class = None
    selected_subject = None

    # ---------- GET: Load students & subjects ----------
    if request.method == 'GET' and request.GET.get('class_id'):
        class_id = request.GET.get('class_id')
        selected_class = SchoolClass.objects.get(id=class_id)
        subjects = Subject.objects.filter(school_class=selected_class)

        if request.GET.get('subject_id'):
            selected_subject = Subject.objects.get(id=request.GET.get('subject_id'))
            students = Student.objects.filter(student_class=selected_class)

            if not students.exists():
                messages.warning(request, "No students found for this class.")

    # ---------- POST: Save attendance ----------
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject')

        selected_class = SchoolClass.objects.get(id=class_id)
        selected_subject = Subject.objects.get(id=subject_id)

        attendance, created = Attendance.objects.get_or_create(
            class_name=selected_class,
            subject=selected_subject,
            teacher=request.user,
            date=date.today()
        )

        if not created:
            messages.error(request, "Attendance already taken today!")
            return redirect('teachers:attandence')

        students = Student.objects.filter(student_class=selected_class)

        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            AttendanceRecord.objects.create(
                attendance=attendance,
                student=student,
                status=True if status == 'Present' else False
            )

        messages.success(request, "Attendance saved successfully!")
        return redirect('teachers:attandence')

    return render(request, 'teachers/attendance.html', {
        'classes': classes,
        'subjects': subjects,
        'students': students,
        'selected_class': selected_class,
        'selected_subject': selected_subject,
    })


# To add the exams
def add_exams(request):
    classes = SchoolClass.objects.all()
    selected_class = None
    exams = None

    if request.method == 'GET' and request.GET.get('class_id'):
        selected_class = SchoolClass.objects.get(id = request.GET.get('class_id'))
        exams = Exam.objects.filter(student_class = selected_class)

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        exam_name = request.POST.get('exam_name')

        selected_class = SchoolClass.objects.get(id=class_id)
        Exam.objects.create(student_class = selected_class, name = exam_name)

        return redirect(f'{request.path}?class_id={class_id}')


    return render(request, 'teachers/exam_list.html', {
        'classes':classes,
        'selected_class':selected_class,
        'exams':exams,
    })

def add_marks(request):
    classes = SchoolClass.objects.all()
    selected_class = None

    subjects = []
    selected_subject = None

    students = []
    exams = []
    selected_exam = None

    if request.method == 'GET' and 'class_id' in request.GET:
        selected_class = SchoolClass.objects.get(id=request.GET.get('class_id'))
        subjects = Subject.objects.filter(school_class=selected_class)
        exams = Exam.objects.filter(student_class=selected_class)
        

        if request.GET.get('subject_id') and request.GET.get('exam_id'):
            
            selected_subject = Subject.objects.get(id=request.GET.get('subject_id'))
            selected_exam = Exam.objects.get(id = request.GET.get('exam_id'))
            students = Student.objects.filter(student_class = selected_class)
                

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')
        exam_id = request.POST.get('exam_id')
        max_marks = request.POST.get('max_marks')

        selected_class = SchoolClass.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)
        exam = Exam.objects.get(id=exam_id)

        students = Student.objects.filter(student_class=selected_class)

        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks :
                Marks.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam=exam,
                    max_marks=max_marks,
                    defaults={
                        'marks_obtained': marks,
                        'teacher': request.user
                    }
                )

        messages.success(request, "Marks saved successfully!")
        return redirect('teachers:add_marks')

    return render(request, 'teachers/add_marks.html', {
        'classes': classes,
        'subjects': subjects,
        'students': students,
        'exams': exams,
        'selected_class': selected_class,
        'selected_subject' : selected_subject,
        'selected_exam': selected_exam
    })