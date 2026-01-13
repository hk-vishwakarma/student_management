from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import StudentForm
from .models import Student
from django.core.paginator import Paginator
from accounts.models import User
from django.contrib import messages
from academics.models import SchoolClass, Subject
from teachers.models import AttendanceRecord, Marks, Exam


def add_student(request):
    classes = SchoolClass.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        class_id = request.POST.get('class_id')
        roll_no = request.POST.get('roll_no')
        date_of_birth = request.POST.get('dob')
        profile_pic = request.POST.get('profile_pic')
        phone = request.POST.get('phone')
        # email = request.POST.get('email')
        
        new_user = User.objects.filter(username=username)
        if new_user.exists():
            messages.warning(request , "Username already exist!")
            return redirect('add_student')
        
        
        user =  User.objects.create_user(
            full_name = full_name,
            username = username,
            password = password,
            role='student'
            
        )
        user.save()
        student_class = SchoolClass.objects.get(id=class_id)
        Student.objects.create(
            user = user,
            full_name = full_name,
            student_class = student_class,
            roll_no = roll_no,
            dob = date_of_birth,
            # email = email,
            phone = phone,
            photo = profile_pic
        )
        return redirect('students:student_list')
        
    return render(request,'students/add_student.html', {'classes': classes})


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
    

# for student can see it's attendence
def student_attendance(request):
    # Get logged-in student
    student = Student.objects.get(user=request.user)

    subject_id = request.GET.get('subject_id')

    attendance_records = AttendanceRecord.objects.filter(student=student).select_related(
        'attendance', 'attendance__subject'
    )
    

    if subject_id:
        # attendance_records = attendance_records.filter(
        #     attendance__subject_id=subject_id
        # )
        subject = Subject.objects.get(id = subject_id)
        attendance_records = attendance_records.filter(attendance__subject = subject)

    subjects = Subject.objects.filter(school_class=student.student_class)

    context = {
        'attendance_records': attendance_records,
        'subjects': subjects,
        'selected_subject': subject_id
    }

    return render(request, 'students/attendance.html', context)


# def student_marks(request):
#     student = Student.objects.get(user=request.user) 
    
#     exams = Exam.objects.filter(student_class=student.student_class)
#     marks_by_exam= None


#     if request.method == 'GET' and request.GET.get('exam_id'):
#         selected_exam = Exam.objects.filter(id = request.GET.get('exam_id'))
#         marks_by_exam = Marks.objects.filter(student = student,exam = selected_exam )


    

#     return render(
#         request,
#         'students/student_marks.html',
#         {'marks_by_exam': marks_by_exam, 'exams':exams}
#     )


def student_marks(request):
    student = Student.objects.get(user=request.user)

    exams = Exam.objects.filter(student_class=student.student_class)

    marks_by_exam = {}

    for exam in exams:
        marks = Marks.objects.filter(
            student=student,
            exam=exam
        ).select_related('subject')

        if marks.exists():
            marks_by_exam[exam] = marks

    return render(
        request,
        'students/student_marks.html',
        {'marks_by_exam': marks_by_exam}
    )