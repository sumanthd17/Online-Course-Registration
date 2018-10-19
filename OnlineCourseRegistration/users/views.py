from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404

from .models import Course

# Create your views here.
class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'Signup.html'

def index(request):
	courses = Course.objects.all()
	context = {'courses': courses}
	for course in courses:
		print(course.max_students)
	return render(request, 'users/home.html', context)

def details(request, course_id):
	course = get_object_or_404(Course, pk=course_id)
	return render(request, 'users/details.html', {'course':course})