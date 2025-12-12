from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
            if user.role == "student":
                return redirect('student_dashboard')
            elif user.role == "teacher":
                return redirect('teacher_dashboard')
            elif user.role == "admin":
                return redirect('admin_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")





def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User added successfully!")
            return redirect('add_user')
    else:
        form = AddUserForm()

    return render(request, 'add_user.html', {'form': form})
