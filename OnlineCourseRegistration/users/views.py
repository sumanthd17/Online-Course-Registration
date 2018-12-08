from django.urls import reverse_lazy,reverse
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.db import IntegrityError, connection
from django.db.models import Count

from .models import Course,Grades, Student,Courseregistrations, FinalStudentRegistrations
from .models import *
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth import *
import requests, json, datetime


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

# def get_user(email, password):
# 	try:
# 		user = CustomUser.objects.get(email=email)
# 	except Exception as e:
# 		user = CustomUser()
# 		user.username = email
# 		user.email = email
# 	user.set_password(password)
# 	user.save()

# 	user = authenticate(username=email, password=password)
# 	return user

def callback(request, token):
	print(token)
	print('req recieved')
	email, password = auth_api(token)
	# user = get_user(email,password)
	# login(request, user)
	# print('successful', email, password)

	user = authenticate(username=email, password=password)
	login(request, user)
	return HttpResponseRedirect('/users')

def auth_api(token):
	try:
		res = requests.post(url=' https://serene-wildwood-35121.herokuapp.com/oauth/getDetails', data={
            'token': token,
            'secret': '1332df120a84c36c569571a7153d38d74f642304a985cc988c965fa225f33af51ee7ffb475897e91dfa7c53e4673487c48894584f5b314a6fffbb9d89f18bad5'
        })
		res = json.loads(res.content)
		email = res['student'][0]['Student_Email']
		password = 'iamstudent'

		print (email, password)
		return email, password

	except Exception as e:
		print(e)
		return None, None

def details(request, course_id):
	course = get_object_or_404(Course, pk=course_id)
	return render(request, 'users/details.html', {'course':course})

def display_students(request):
	students = Student.objects.all()
	context = {'students': students}
	return render(request, 'users/students.html', context)

def add_student(request):
	if request.method == 'POST':
		student = Student()
		student.name = request.POST.get('name')
		student.roll = request.POST.get('roll_number')
		student.email = request.POST.get('mail')
		student.year = request.POST.get('year')
		student.save()
		print(student.roll, student.year)

	else:
		print('error in request')

	students = Student.objects.all()
	context = {'students': students}
	return render(request, 'users/students.html', context)

def add_course(request):
	if request.method == 'POST':
		course = Course()
		course.course_id = request.POST.get('id')
		course.course_name = request.POST.get('name')
		course.course_prof = request.POST.get('prof')
		course.course_type = request.POST.get('type')
		course.course_rigour = request.POST.get('rigour')
		course.course_level = request.POST.get('level')
		course.course_hasprereqs = request.POST.get('pre_req')
		course.course_delivery_mode = request.POST.get('delivery_mode')
		course.course_description = request.POST.get('description')
		course.course_credits = request.POST.get('credits')
		#students = request.POST.get('max_students')
		try:
			course.course_max_students = request.POST.get('max_students')
		#course.max_students = int(request.POST.get('max_students', ''))
		except ValueError:
			course.course_max_students = 0

		course.save()
		return HttpResponseRedirect('/users')
	else:
		return HttpResponseRedirect('/users')

def add_course_details(request, course_id):
	#details = get_object_or_404(Detail, pk=course_id)
	# details = Detail.objects.get(pk=course_id)
	# details = Detail.objects.create(pk=course_id)
	# print(details.min_GPA)
	if request.method == 'POST':
		course = Course.objects.get(course_id=course_id)
		course.course_name = request.POST.get('name')
		course.course_prof = request.POST.get('prof')
		try:
			course.course_max_students = request.POST.get('max_students')
		#course.max_students = int(request.POST.get('max_students', ''))
		except ValueError:
			course.course_max_students = 0
		course.course_rigour = request.POST.get('rigour')
		course.course_level = request.POST.get('level')
		course.course_hasprereqs = request.POST.get('pre_req')
		course.course_delivery_mode = request.POST.get('delivery_mode')
		course.course_description = request.POST.get('description')
		course.save()
		# details = Detail.objects.create(course_id=course_id, min_GPA=request.POST.get('min_GPA'), description=request.POST.get('description'))
		# # details = Detail.objects.get(pk=course_id)
		# details.min_GPA = request.POST.get('min_GPA')
		# details.description = request.POST.get('description')
		# details.save()
		print(course.course_name)
	# print(details.min_GPA, details.description)
		return HttpResponseRedirect('/users')
	else:
		return HttpResponseRedirect('/users')

def special_req(request, course_id):
	print('req recieved', course_id)
	if request.method == 'POST':
		special_req = BufferSpecialPermissionsTable.objects.create(course_id=course_id, req=request.POST.get('req'))

		# special_req = SpecialPermissions.objects.create(course_id=course_id, req=request.POST.get('req'))
		special_req.save()
		print(special_req.id, special_req.req)
	else:
		print('req failed')

	special_reqs = SpecialPermissions.objects.all()
	context = {'special_reqs':special_reqs}

	return HttpResponseRedirect('/users')

def approve_req(request):
	special_reqs = BufferSpecialPermissionsTable.objects.all()
	context = {'special_reqs': special_reqs}
	return render(request, 'users/approve_req.html', context)

def special_req_res_acc(request, request_id):
	special_req = get_object_or_404(BufferSpecialPermissionsTable, pk=request_id)
	special_req.status = 'Accepted'
	special_req.save()
	special_reqs = BufferSpecialPermissionsTable.objects.all()
	context = {'special_reqs': special_reqs}
	return render(request, 'users/approve_req.html', context)

def special_req_res_dec(request, request_id):
	special_req = get_object_or_404(BufferSpecialPermissionsTable, pk=request_id)
	special_req.status = 'Declined'
	special_req.save()
	special_reqs = BufferSpecialPermissionsTable.objects.all()
	context = {'special_reqs': special_reqs}
	return render(request, 'users/approve_req.html', context)

def audit_course(request):
	if request.method == 'POST':
		auditcourse = AuditCourse()
		auditcourse.name = request.POST.get('name')
		auditcourse.roll = request.POST.get('roll')
		auditcourse.save()
		return HttpResponseRedirect('/users')
	else:
		return render(request, 'users/audit.html')

def publish_course_registrations(request):
	if request.method == 'POST':
		cid=request.POST.get('course')
		with connection.cursor() as cursor:
			cursor.execute('select final_studentregistrations_cid from FinalStudentRegistrations where exists (select final_studentregistrations_cid from FinalStudentRegistrations where final_studentregistrations_cid ='+str(cid)+')')
			x = cursor.fetchall()
			if len(x) == 0:
				cursor.execute("select studentRegistrations.studentRegistrations_id, studentRegistrations.studentRegistrations_cid, studentRegistrations.studentRegistrations_sid, Student.Student_cgpa, Student.Student_current_year from studentRegistrations inner join Student on Student.Student_roll_no = studentRegistrations.studentRegistrations_sid where studentRegistrations_cid = "+str(cid)+" order by Student_current_year DESC, Student_cgpa DESC limit 4")
				row = cursor.fetchall()
				print('row/n')
				print(len(row))
				print(row)
				l=[]
				m=[]
				for i in range(len(row)):
					final = FinalStudentRegistrations()
					s=Student.objects.get(student_roll_no=row[i][2])
					c=Course.objects.get(course_id=row[i][1])
					final.final_studentregistrations_sid = s
					final.final_studentregistrations_cid = c
					final.final_studentregistrations_last_updated = datetime.datetime.now()
					final.save()
					print(s)
					print(c)
					l.append(s)
					m.append(c)
				g={'student':l}
				return render(request, 'users/publish_course_registrations.html',g)
			else :
				cursor.execute("select final_studentregistrations_sid from FinalStudentRegistrations where final_studentregistrations_cid ="+str(cid))
				row = cursor.fetchall()
				l = []
				for i in range(len(row)):
					s=Student.objects.get(student_roll_no=row[i][0])
					print(s)
					l.append(s)
				g={'student':l}

				return render(request, 'users/publish_course_registrations.html',g)
	else:
		return render(request, 'users/publish_course_registrations.html')


def ClassRoaster(request):
	if request.method == 'POST':
		register = list(Register.objects.all())
		reg = []
		for i in register:
			reg.append(str(i).split(' - '))
	return render(request,'users/faculty.html')

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
		
class CourseListView(View):
	model=Courseregistrations
	template_name="users/register.html"
				
	def get(self, request, *args, **kwargs):
		#queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').prefetch_related('
		queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
		#values_list('course.course_id','course.course_name','course.course_credits')

		#queryvals['test']=1
		context={}
		context['queryvals']=queryvals
		myname=request.user
		student=Student.objects.values('student_roll_no','student_first_name','student_last_name','student_cur_year','student_curr_sem').filter(student_email=myname)
		for i in student:
			fname = i['student_first_name']			
			lname = i['student_last_name']
			name = fname+" "+lname
			context['name']=name
			context['student_roll_no']=i['student_roll_no']
			context['student_cur_year']=i['student_cur_year']
			context['student_cur_sem']=i['student_curr_sem']
		return render(request, self.template_name,context)
			
	def post(self, request, *args, **kwargs):
		if 'saveCourseBtn' in request.POST:
			courseregistrations_cid = request.POST.getlist('saveCourse')
			myname = request.POST.getlist('saveCourseBtn')
			myfaculty = request.POST.getlist('fid')
			try:				
				student_id = CustomUser.objects.values('id').filter(username=myname[0])
				#print(student_id)
				for i in student_id:
					sid = i['id']
					#print(sid)
				student_no = Student.objects.values('student_roll_no').filter(student_Id=sid)
				for s in student_no:
					student_roll = s['student_roll_no']
				#print(student_roll)	
				course = get_object_or_404(Course, pk=courseregistrations_cid[0])	
				student = get_object_or_404(Student, pk=student_roll)
				print("Now insert record!!")		
				tablesave = Studentregistrations.objects.create(studentregistrations_cid=course, studentregistrations_sid=student,studentregistrations_status='S')
				print("Record saved")
				tablesave = Studentregistrations.objects.create(studentregistrations_cid=course, studentregistrations_sid=student,studentregistrations_status='S')
				queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.success(request, 'Course record saved successfully!')
			except IntegrityError as e:
				print(e)
				queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Record already exists!! Please select another record')
			except IndexError as e:
				queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Please select a course to save!!')		
			return render(request,self.template_name,{'queryvals': queryvals})
		elif 'submitCourseBtn' in request.POST:
			courseregistrations_cid = request.POST.getlist('saveCourse')
			myname = request.POST.getlist('saveCourseBtn')
			myname = request.POST.getlist('submitCourseBtn')
			myfaculty = request.POST.getlist('fid')
			print(courseregistrations_cid)
			print(myname)
			print(myfaculty)

			try:				
				student_id = CustomUser.objects.values('id').filter(username=myname[0])
				#print(student_id)
				for i in student_id:
					sid = i['id']
					#print(sid)
				student_no = Student.objects.values('student_roll_no').filter(student_Id=sid)
				for s in student_no:
					student_roll = s['student_roll_no']

				#print(student_roll)	
				course = get_object_or_404(Course, pk=courseregistrations_cid[0])	
				student = get_object_or_404(Student, pk=student_roll)
				checkStatus = Studentregistrations.objects.filter(studentregistrations_sid__in [student_roll]).distinct().values('studentregistrations_status').annotate(status_count=Count('studentregistrations_status')).filter(studentregistrations_status__gt=1).order_by('studentregistrations_status')
				for status in checkStatus:
					x = status['status_count']
				if(x > 0):
					queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
					messages.error(request,'Your Registration already completed!! Wait for Add/Drop Course')

				print(student_roll)	
				course = get_object_or_404(Course, pk=courseregistrations_cid[0])	
				student = get_object_or_404(Student, pk=student_roll)
				checkStatus = Studentregistrations.objects.filter(studentregistrations_sid__in=[student_roll],studentregistrations_status='R').values('studentregistrations_status').annotate(status_count=Count('studentregistrations_status'))
				print(checkStatus)
				if checkStatus:
					for status in checkStatus:
						x = status['status_count']
					if(x > 0):
						queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
						messages.error(request,'Your Registration already completed!! Wait for Add/Drop Course')

				else:
					tablesave = Studentregistrations.objects.update_or_create(studentregistrations_cid=course, studentregistrations_sid=student,studentregistrations_status='R')
					tablesave = Studentregistrations.objects.all().update(studentregistrations_status='R')
					queryvals =  Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
					messages.error(request,'Registration of courses completed! Wait for Add/Drop course phase for further updates')
			except IntegrityError as e:
				queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Record already exists! Choose another course and submit')
			except IndexError as e:
				queryvals =Courseregistrations.objects.all().select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Please select a course and submit!!')

			return render(request,self.template_name,{'querysets': querysets})					
		
	def coursedetails(request,course_id,val):
		course = get_object_or_404(Course, pk=course_id)
		cid=course_id
		print(course.course_description," ",course.course_name)
		querysets=Course.objects.filter(course_id=cid).only("course_id", "course_name","course_delivery_mode","course_pre_req","course_type","course_credits")
		return render(request,"users/coursedetails.html",{'querysets': querysets})
		#return HttpResponseRedirect('/users/coursedetails.html')
		 
		"""except Exception as e:
			print(e)"""
		return render(request,self.template_name,{'queryvals': queryvals})					
		
	def coursedetails(request,course_id,val):
		print(course_id)
		print(val)
		queryvals =Courseregistrations.objects.filter(courseregistrations_cid=course_id,courseregistrations_fid=val).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
		return render(request,"users/coursedetails.html",{'queryvals': queryvals})


class StudentCourseListView(View):
	model=Studentregistrations
	template_name="users/studenthome.html"
	context_object_name = 'clist'
			
	def get(self, request, *args, **kwargs):
		queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values_list('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits')
		#values_list('course.course_id','course.course_name','course.course_credits')
		return render(request, self.template_name,{'queryvals': queryvals})	
		
