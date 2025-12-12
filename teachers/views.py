from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Teacher

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
        user = User.objects.create_user(username=username, password=password)
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
