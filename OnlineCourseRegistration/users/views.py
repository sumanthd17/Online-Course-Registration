from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Course, Detail, Grade

# Create your views here.
class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'Signup.html'

def index(request):
	courses = Course.objects.all()
	total_courses = len(Course.objects.all())
	print(total_courses)
	context = {'courses': courses, 'total_courses': total_courses}
	return render(request, 'users/home.html', context)

def details(request, course_id):
	course = get_object_or_404(Course, pk=course_id)
	return render(request, 'users/details.html', {'course':course})

def add_course(request):
	if request.method == 'POST':
		course = Course()
		course.name = request.POST.get('name')
		course.prof = request.POST.get('prof')
		#students = request.POST.get('max_students')
		try:
			course.max_students = request.POST.get('max_students')
		#course.max_students = int(request.POST.get('max_students', ''))
		except ValueError:
			course.max_students = 0

		course.save()
		return HttpResponseRedirect('/users')
	else:
		return HttpResponseRedirect('/users')

def add_grade(request):
	if request.method == 'POST':
		grade = Grade()
		grade.student_id = request.POST.get('user_id')
		grade.course = request.POST.get('course')
		grade.grade_point = request.POST.get('grade_point')
		grade.save()
		return HttpResponseRedirect('/users')
	else :
		return HttpResponseRedirect('/users')

def add_course_details(request, course_id):
	print('req recieved')
	#details = get_object_or_404(Detail, pk=course_id)
	#details = Detail.objects.get(pk=course_id)
	# details = Detail.objects.create(pk=course_id)
	print(course_id)
	if request.method == 'POST':
		details = Detail.objects.create(course_id=course_id, min_GPA=request.POST.get('min_GPA'), description=request.POST.get('description'))
		# details.min_GPA = request.POST.get('min_GPA')
		# details.description = request.POST.get('description')
		details.save()
		print(details.min_GPA, details.description)
		return HttpResponseRedirect('/users')
	else:
		return HttpResponseRedirect('/users')
