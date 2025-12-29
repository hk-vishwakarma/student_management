from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolClass
from .models import SchoolClass, Subject

# Create your views here.

def class_list(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        if class_name:
            SchoolClass.objects.get_or_create(name=class_name)
            messages.success(request, "Class added successfully!")
            return redirect('academics:class_list')

    classes = SchoolClass.objects.all()
    return render(request, 'academics/class_list.html', {'classes': classes})




def manage_subjects(request):
    classes = SchoolClass.objects.all()
    selected_class = None
    subjects = None

    if request.method == 'GET' and request.GET.get('class_id'):
        selected_class = SchoolClass.objects.get(id=request.GET.get('class_id'))
        subjects = Subject.objects.filter(school_class=selected_class)

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        subject_name = request.POST.get('subject_name')

        selected_class = SchoolClass.objects.get(id=class_id)
        Subject.objects.create(
            school_class=selected_class,
            name=subject_name
        )
        return redirect(f"/academics/subjects/?class_id={class_id}")

    return render(request, 'academics/subject_manage.html', {
        'classes': classes,
        'selected_class': selected_class,
        'subjects': subjects
    })
