from datetime import datetime
import email
from msilib.schema import Class
from pyexpat import model
from statistics import mode
from django.db import models
# course model 
# student model 
# teacher model
# assignment model
# solution model


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):

    firstname = models.CharField(max_length=100, default="")
    lastname = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=100, default="")
    identity = models.CharField(max_length=100, default="")
    PRN = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=100, default="")
    courses = models.ManyToManyField(Course, default="")
    
    def __str__(self):
        return self.firstname+" "+self.lastname


class Teacher(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default="")
    identity = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    isadmin = models.BooleanField(default=False)
    

    def __str__(self):
        return self.firstname+" "+self.lastname


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    question = models.FileField(upload_to="assignments/pdf")
    instruction = models.CharField(max_length=200, default="")
    deadline = models.DateField()
    maxmarks = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Submission(models.Model):
    answer = models.FileField(upload_to="solutions/pdf")
    # answer = models.CharField(max_length=200)
    roll = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    isevaluated = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


