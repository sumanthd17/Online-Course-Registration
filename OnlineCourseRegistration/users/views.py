from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Course

# Create your views here.
class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'Signup.html'

def index(request):
	courses = Course.objects.all()
	context = {'courses': courses}
	return render(request, 'users/home.html', context)

def details(request, course_id):
	course = get_object_or_404(Course, pk=course_id)
	return render(request, 'users/details.html', {'course':course})

def add_course(request):
	print('req came')
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
		print('data saved')
		return HttpResponseRedirect('/users')
	else:
		return render(request, 'users/')