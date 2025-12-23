from django.shortcuts import render, redirect

# Create your views here.
def admin_dashboard(request):
    if not request.user.is_superuser :
        return redirect('login')
    return render(request, "dashboard/admin_dashboard.html")

def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")

def teacher_dashboard(request):
    return render(request, "dashboard/teacher_dashboard.html")