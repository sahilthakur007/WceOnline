from hmac import new
from multiprocessing import context
import string
from urllib import request
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            return redirect("studentHome")

        except:
            return redirect("allSubjects")
    return render(request, "home.html")


@login_required(login_url='home')
def listAllSubjects(request):

    teacher = Teacher.objects.get(username=request.user.username)
    allsubjects = teacher.courses.all()

    print(id)
    context = {
        "subjects": allsubjects,
    }
    return render(request, "list_all_subjects.html", context)


@login_required(login_url='home')
def studentHome(request):
    student = Student.objects.get(username=request.user.username)
    allsubjects = student.courses.all()
    context = {
        "subjects": allsubjects,
    }
    return render(request, "homeStudent.html", context)


@login_required(login_url='home')
def listAllAssignmentForSubjects(request, course_id):
    students = Student.objects.all()
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(username=request.user.username)
    allAssignments = course.assignment_set.all()
    print(teacher)

    form = AssignmentCreateForm()
    if request.method == "POST" and request.POST.get('select-student-prn'):
        prn = request.POST.get('select-student-prn')
        student = Student.objects.get(id=prn)
        student.courses.add(course)
        student.save()
        messages.info(request, 'Student added successfully.')

    elif request.method == "POST":

        form = AssignmentCreateForm(request.POST, request.FILES)

        if form.is_valid():
            newAssignments = form.save(commit=False)
            newAssignments.course = course
            newAssignments.teacher = teacher
            newAssignments.save()
            form = AssignmentCreateForm()
            messages.info(request, 'Assignment added successfully.')
            redirect(reverse('allAssignments', args=[course_id]))

        else:
            messages.info(request, "Enter valid date format")
    context = {
        "assignments": allAssignments,
        "form": form,
        "students": students
    }
    return render(request, "list_all_assignments_for_subject.html", context)


@login_required(login_url='home')
def listAllAssignmentForSubjectsStudent(request, course_id):
    course = Course.objects.get(id=course_id)
    allAssignments = course.assignment_set.all()
    context = {
        "assignments": allAssignments,
    }
    return render(request, "allAssignmentsStudent.html", context)


@login_required(login_url='home')
def listAllSolutionForAssignment(request, assignment_id):

    # print(allSollutions)
    solution = {}
    if request.method == "POST":
        marks = request.POST['marks']
        solution_id = request.POST['solution_id']
        solution = Submission.objects.get(id=solution_id)
        solution.score = marks
        solution.isevaluated = True
        solution.save()
    assignment = Assignment.objects.get(id=assignment_id)
    allSollutions = assignment.submission_set.all()
    print(allSollutions)
    context = {
        "sollutions": allSollutions,
        "solution": solution
    }
    return render(request, "list_all_solutions_for_assignment.html", context)


@login_required(login_url='home')
def singleAssignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    student = Student.objects.get(username=request.user.username)
    solutions = assignment.submission_set.all()

    try:
        currentUserSolutions = solutions.get(student=student)
        print(currentUserSolutions)
    except:
        currentUserSolutions = ""

    # if solutions.get(student=student):
        # currentUserSolutions = solutions.get(student=student)

    form = SolutionCreationForm()
    if request.method == "POST" and currentUserSolutions:
        # print("true")
        # print("true")
        answer = request.FILES['answer']
        name = request.POST['name']
        currentUserSolutions.answer = answer
        currentUserSolutions.name = name
        currentUserSolutions.save()
        messages.info(request, 'Assignment updated successfully.')


    elif(request.method == "POST"):
        form = SolutionCreationForm(request.POST, request.FILES)
        print(request.FILES['answer'])
        if form.is_valid():
            print("true")
            newSollution = form.save(commit=False)
            newSollution.student = student
            newSollution.assignment = assignment
            newSollution.roll = student.PRN
            newSollution.save()
            currentUserSolutions = newSollution
            form = SolutionCreationForm()
            messages.info(request, 'Assignment submitted successfully.')

        else:
            print(form.errors)
    context = {
        "form": form,
        "assignment": assignment,
        "sollution": currentUserSolutions
    }
    return render(request, "singleAssignmentStudent.html", context)


def registerFaculty(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            return redirect("studentHome")

        except:
            return redirect("allSubjects")

    form = RegistrationForm()
    # print(form)
    if request.method == "POST":
        print("true")
        form = RegistrationForm(request.POST)
        roll = request.POST['roll']
        print(roll)
        if form.is_valid():
            user = form.save()
            print(form)
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            username = request.POST['username']

            user.set_password(user.password)
            user.save()
            if roll == "Teacher":
                Teacher.objects.create(
                    firstname=firstname, lastname=lastname, email=email, password=password, identity="TEACHER", username=username)
                return redirect("loginTeacher")
            else:
                PRN = request.POST['prn']
                Student.objects.create(
                    firstname=firstname, lastname=lastname, email=email, password=password, identity="STUDENT", username=username, PRN=PRN)
                return redirect("loginStudent")
        else:
            print(form.errors)
            return render(request, "signup.html", {"err": form.errors, "form": form})

    context = {
        "form": form
    }
    return render(request, "signup.html", context)


def loginStudent(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            # login(request, user)
            return redirect("studentHome")

        except:
            return redirect("allSubjects")
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username+" "+password)

        user = authenticate(username=username, password=password)

        # teacher.filter
        if user is not None:
            try:
                student = Student.objects.get(username=user.username)
                login(request, user)
                return redirect("studentHome")
            except:
                   messages.info(request, "Login failed!")

        else:
            messages.info(request, "Login failed!")

    return render(request, "studentlogin.html", {})


def loginTeacher(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            return redirect("studentHome")

        except:
               return redirect("allSubjects")  

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username+" "+password)

        user = authenticate(username=username, password=password)
        print(user)
        # teacher.filter
        if user is not None:
            try:
                teacher = Teacher.objects.get(username=user.username)
                login(request, user)
                return redirect("allSubjects")
            except:
                  messages.info(request, "Login failed!")

        else:
            messages.info(request, "Login failed!")

    return render(request, "studentlogin.html", {})

def adminLogin(request):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(username=request.user.username)
            return redirect("studentHome")

        except:
               teacher = Teacher.objects.get(username=user.username)
               if teacher.isadmin:
                   return redirect("facultylist")
               else:
                    return redirect("allSubjects")
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        # print(username+" "+password)

        user = authenticate(username=username, password=password)
        print(user)
        # teacher.filter
        if user is not None:
            try:
                teacher = Teacher.objects.get(username=user.username)
                if(teacher.isadmin):
                    login(request, user)
                    return redirect("facultylist")
                else:
                     messages.info(request, "Login failed!")
            except:
                messages.info(request, "Login failed!")

        else:
            messages.info(request, "Login failed!")

    return render(request, "adminLogin.html", {})

@login_required(login_url='home')
def logoutuser(request):
    logout(request)
    return redirect("home")


@login_required(login_url='home')
def evaluateAssignment(request, submission_id):
    if request.method == "POST":
        marks = request.POST['marks']
        solution_id = request.POST['solution_id']
        print(solution_id+" "+marks)
        submission = Submission.objects.get(id=submission_id)

@login_required(login_url='home')     
def listAllFaculty(request):
    teachers =Teacher.objects.all()
    courses  = Course.objects.all()
    # print(teachers)
    # print(courses)
    
    if request.method =="POST":
        
        try:
            newCourse = request.POST["newcourse"]
        except:
               newCourse = ""
        if newCourse:
                     try:
                         course = Course.objects.get(name=newCourse)
                         messages.info(request, "Subject alredy present")
                     except:
                            Course.objects.create(name= newCourse)
                            messages.info(request,"Course added sussesfully")
        else:    
            teacher_id = request.POST["teacher_id"]
            course_id = request.POST["course_id"]
            print(teacher_id+" "+course_id)
        
            teacher =Teacher.objects.get(id=teacher_id)
            course =Course.objects.get(id=course_id)
            teacher.courses.add(course)
            teacher.save()
            messages.info(request, 'Course assigned successfully.')

    context={
        "teachers":teachers,
        "courses":courses,
    }
    return render(request,"adminFacultyList.html",context)

