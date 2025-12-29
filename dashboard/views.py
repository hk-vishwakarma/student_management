from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_superuser :
        return redirect('login')
    return render(request, "dashboard/admin_dashboard.html")

@login_required(login_url='login')
def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")

@login_required(login_url='login')
def teacher_dashboard(request):
    return render(request, "dashboard/teacher_dashboard.html")