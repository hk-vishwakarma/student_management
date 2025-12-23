from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddUserForm
from django.contrib.auth.hashers import make_password

# Create your views here.
def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check user role and redirect accordingly
            if user.is_superuser :
                return redirect('admin_dashboard')
            elif user.role == "student":
                return redirect('student_dashboard')
            elif user.role == "teacher":
                return redirect('teacher_dashboard')
            

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")



def logout_view(request):
    logout(request)
    return redirect('login')
