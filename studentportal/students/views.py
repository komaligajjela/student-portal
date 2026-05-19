from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import csv
from django.http import HttpResponse

# Home Page
def home(request):

    total_students = Student.objects.count()

    return render(
        request,
        'students/home.html',
        {
            'total_students': total_students
        }
    )


# Student List
def student_list(request):

    query = request.GET.get('q')

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(course__icontains=query)
        )

    paginator = Paginator(students, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request,
                  'students/student_list.html',
                  {
                      'page_obj': page_obj
                  })

# Add Student
@login_required
def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})


# Update Student
@login_required
def update_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'students/update_student.html', {'form': form})


# Delete Student
@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'students/delete_student.html', {'student': student})

def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

    return render(request, 'students/login.html')


def logout_user(request):

    logout(request)

    return redirect('login')

def export_csv(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename=students.csv'

    writer = csv.writer(response)

    writer.writerow([
        'Name',
        'Email',
        'Course',
        'Age',
        'Joined Date'
    ])

    students = Student.objects.all()

    for student in students:

        writer.writerow([
            student.name,
            student.email,
            student.course,
            student.age,
            student.joined_date
        ])

    return response