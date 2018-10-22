from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse,request,response
from django.http import JsonResponse
from django.shortcuts import render,redirect,render_to_response
from rest_framework import serializers
import logging


from users.forms import CustomUserCreationForm
from OnlineCourseRegistration.models import AcademicCourse
from OnlineCourseRegistration.forms import GetCourseList


# Create your views here.



class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'Signup.html'
	

class CourseListView(generic.ListView):
	model = AcademicCourse
	template_name="courselist.html"
	context_object_name = 'clist'
		
	def get_queryset(self):
		print(self.request.method)
		queryset = AcademicCourse.objects.filter().only("academic_course_id", "academic_course_name")
		return queryset;				
