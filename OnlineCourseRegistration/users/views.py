from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Course, Detail, Grade, Student, AuditCourse, AcademicCourse, Register, final_Register
from django.views import View
import operator


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

def add_student(request):
	if request.method == 'POST':
		student = Student()
		student.name = request.POST.get('name')
		student.roll = request.POST.get('roll_number')
		student.email = request.POST.get('mail')
		student.year = request.POST.get('year')
		student.save()
		#print(student.roll, student.year)

	else:
		print('error in request')

	students = Student.objects.all()
	context = {'students': students}
	return render(request, 'users/students.html', context)

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

def audit_course(request):
	if request.method == 'POST':
		auditcourse = AuditCourse()
		auditcourse.name = request.POST.get('name')
		auditcourse.roll = request.POST.get('roll')
		auditcourse.save()
		return HttpResponseRedirect('/users')
	else:
		return render(request, 'users/audit.html')

def publish_course_registration(request):
	if request.method == 'POST':
		subject = request.POST.get('course')
		print('subject')
		print(subject)
		course = list(Course.objects.all())
		c = []
		#print('course')
		#print(course)
		for i in course:
			c.append(str(i).split(' - '))
		for i in c:
			if subject in i:
				max = i[-1]
				break
		#print('max')
		#print(max)
		student_list = []
		student = list(Student.objects.all())
		#print('student')
		#print(student)
		for i in student:
			student_list.append(str(i).split(' - '))
		student_list_sel = []
		#print('student_list')
		#print(student_list)
		"""for i in student_list:
			if subject in i:
				student_list_sel.append(i)
		"""
		register = list(Register.objects.all())
		reg = []
		for i in register:
			reg.append(str(i).split(' - '))
		for i in reg:
			if subject in i:
				student_list_sel.append(i)
		#print('student_list_sel')
		#print(student_list_sel)
		enroll_dict = {}
		#print('reg')
		#print(reg)
		for i in student_list_sel:
			for j in student_list:
				if i[0] == j[1]:
					enroll_dict[i[0]] = j[-1]
		#print('enroll_dict')
		#print(enroll_dict)
		enroll_sorted = sorted(enroll_dict.items(), key=lambda kv:kv[1], reverse=True)
		#print('enroll_sorted')
		#print(enroll_sorted)
		enroll_list = []
		#print('len')
		#print(len(enroll_list))
		for i in range(len(enroll_sorted)):
			enroll_list.append(enroll_sorted[i][0])
		print(enroll_list)

		for i in range(len(enroll_list)):
			final = final_Register()
			final.student_id = enroll_list[i]
			final.course=subject
			final.save()
		li=[]
		for i in list(final_Register.objects.filter(course=subject)):
			k=str(i).split(' - ')
			li.append(k)
		final={'x':enroll_list , 'sub':subject}
		print(final)
	return render(request, 'users/publish_course_registrations.html',final)

def view_registration(request):
	roll_no='S20160020125'
	li=[]
	for i in list(final_Register.objects.filter(student_id='S20160020125')):
		k=str(i).split(' - ')
		li.append(k)
	print(li)
	lis=[]
	for i in range(len(li)):
		lis.append(li[i][1])
	lis=unique(lis)
	final={'x':lis}
	print(final)
	return render(request, 'users/view_registrations.html',final)

def unique(list1): 
	unique_list = [] 
	for x in list1:
		if x not in unique_list:
			unique_list.append(x)
	return unique_list
def faculty(request):
	print('yes')
	return render(request, 'users/faculty.html')
		
class CourseListView(View):
	model=AcademicCourse
	template_name="users/Students.html"
	context_object_name = 'clist'
		
	def get(self, request, *args, **kwargs):
		print(self.request.method)
		print("Received request in CourseListView: "+self.request.method)
		querysets = AcademicCourse.objects.filter().only("academic_course_id", "academic_course_name")			
		return render(request, self.template_name,{'querysets': querysets})
	
	def post(self, request, *args, **kwargs):
		print("Received post request")
		idval = request.POST['cid']
		print("In post id is "+str(idval))