from dataclasses import field
from distutils.command.build_scripts import first_line_re
from logging import PlaceHolder
from tkinter import Widget
from tkinter.ttk import Style
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class RegistrationForm(forms.ModelForm):
	# first_name: forms.CharField(max_length=100,  widgets=forms.TextInput(
	# 	attrs={'class': 'form-control'}))
	# last_name: forms.CharField(max_length=100, widgets=forms.TextInput(
	# 	attrs={'class': 'form-control form-input'}))
	# email: forms.EmailField(widget=forms.EmailInput(
	# 	attrs={'class': 'form-control form-input'}))
	# username: forms.CharField(max_length=100, widget=forms.TextInput(
	# 	attrs={'class': 'form-control form-input'}))
	# password: forms.CharField(max_length=100, widget=forms.PasswordInput(
	# 	attrs={'class': 'form-control form-input'}))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control form-input-fname', 'placeholder': 'firstname','required':'true'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control form-input-lname', 'placeholder': 'lastname','required':'true'}),
			'username': forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'username','required':'true'}),
			'email': forms.EmailInput(attrs={'class': 'form-control form-input', 'placeholder': 'email','required':'true'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control form-input', 'placeholder': 'password','required':'true'}),



		}


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'email', 'password', 'mobile']


class DatePickerInput(forms.DateInput):
    input_type = 'date'
class AssignmentCreateForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['title', 'question', 'instruction', 'deadline', "maxmarks"]
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'Title Of Assignment'}),
			'question': forms.FileInput(attrs={'class': 'form-control form-input'}),
			'instruction': forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'Instruction to submit'}),
			'maxmarks': forms.NumberInput(attrs={'class': 'form-control form-input', 'placeholder': 'Maximum Marks For assignent'}),
			'deadline': DatePickerInput(attrs={'class': 'form-control form-input'}),
			

		}


class SolutionCreationForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields =["name","answer"]
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'Title Of Assignment','required':'true'}),
			'answer': forms.FileInput(attrs={'class': 'form-control form-input','style':'margin:0px 2vw','required':'true'}),

		}
