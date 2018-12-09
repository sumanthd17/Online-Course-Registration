from django.urls import reverse_lazy,reverse
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count,Sum
from django.db import connection

from .models import Course,Grades, Student,Courseregistrations,RegistrationPolicy,Studentregistrations
from .models import *
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth import *
import requests, json
from datetime import datetime as dt
from datetime import timedelta
import pytz


from django.views import View
import operator




def add_sprofile(request):
	print("Now add student profile")
	if request.method == 'POST':
		fname=request.POST.get('fname')
		lname=request.POST.get('lname')
		roll_number=request.POST.get('roll_number')
		mail=request.POST.get('mail')
		mygender=request.POST.get('gender')
		mydob=request.POST.get('dob')
		regyear=request.POST.get('regyear')
		mob=request.POST.get('mobile')
		year=request.POST.get('year')	
		sem=request.POST.get('sem')
		myid=request.POST.get('uid')
		user=get_object_or_404(CustomUser,pk=myid)	
		if user:
			student=Student.objects.update_or_create(student_roll_no=roll_number,student_first_name=fname,student_last_name=lname,student_email=mail,student_gender=mygender,student_dob=mydob,student_mobile=mob,student_reg_year=regyear,student_cur_year=year,student_curr_sem=sem,student_degree="B.Tech",student_degree_duration="4 years",student_Id=user)
			messages.success(request,"Profile created")
		else:
			messages.error(request,"Profile Creation failed!Please check logs")
	return HttpResponseRedirect('/users/login.html')
	

# Create your views here.
class SignUp(generic.CreateView):
	template_name = 'Signup.html'
	model=CustomUser
	def get(self, request, *args, **kwargs):
		form_class = CustomUserCreationForm
		print("Getting Singup page now")
		return render(request, 'users/Signup.html', {'form':form_class})
	def post(self, request, *args, **kwargs):
		form = CustomUserCreationForm(request.POST)
		print("post signup data")
		if form.is_valid():
			print("Valid form")			
			print("clicked signup")
			user = form.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			print("authenticated")
			me = form.cleaned_data
			if me['role']=='student':
				print("I am a student")
				student=Student.objects.filter(student_email=me['email']).values('student_roll_no')
				if student:					
					return HttpResponseRedirect('/users/login.html')
				else:
					print("I am a new student")
					return HttpResponseRedirect('/users/profile.html')
		else:
			messages.error(request,"Please add all values as per help")
			return render(request, 'users/Signup.html', {'form': form})
	   		
class Login(generic.CreateView):
	model=CustomUser
	template_name="/users/login.html/"	
	def get(self, request, *args, **kwargs):
		context={}
		print("Getting login page now")
		return render(request, 'users/login.html', context)
	
	def post(self, request, *args, **kwargs):
   		if 'loginBtn' in request.POST:
   			print("Let me login")
   			context={}
   			myname=request.POST.get("username")
   			pwd=request.POST.get("password")
   			role=request.POST.get("role")
   			print(myname)
   			print(pwd)
   			print(role)   			
   			user = authenticate(username=myname, password=pwd)
   			print(user)
   			if user:
   				print("Authenticated")
   				if role=='student':
   					print("I am a student")
   					login(request,user)
   					return HttpResponseRedirect('/users/studenthome.html')  					
   				elif role=='admin':
   					login(request,user)
   					return HttpResponseRedirect('/home.html') 
   					#return HttpResponseRedirect('/some/where')    				
   			else:
   				print("Not authenticated")
   				return render(request,'users/login.html/',{})
   			


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
		#print(student.roll, student.year)

	else:
		print('error in request')

	students = Student.objects.all()
	context = {'students': students}
	return render(request, 'users/students.html', context)

def add_course(request):
	if request.method == 'POST':
		course = Course()
		course.course_name = request.POST.get('name')
		course.course_prof = request.POST.get('prof')
		course.course_type = request.POST.get('type')
		course.course_rigour = request.POST.get('rigour')
		course.course_level = request.POST.get('level')
		course.course_hasprereqs = request.POST.get('pre_req')
		course.course_delivery_mode = request.POST.get('delivery_mode')
		course.course_description = request.POST.get('description')
		course.course_credits = request.POST.get('credits')
		course.course_offeredYear = request.POST.get('offeredYear')
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
		try:
			grade = Grades()
			studentid = request.POST.get('user_id')
			courseid = request.POST.get('course')
			coursestatus = request.POST.get('status')
			coursegrade = request.POST.get('grade_point')
			student=get_object_or_404(Student,pk=studentid)
			course=get_object_or_404(Course,pk=courseid)
			myemail=request.user
			user=CustomUser.objects.values('id').filter(email=myemail)
			for x in user:
				uid=x['id']
			user=get_object_or_404(CustomUser,pk=uid)
			print(user)
			sreg = Studentregistrations.objects.filter(studentregistrations_cid=courseid,studentregistrations_sid=studentid).values('studentregistrations_status')
			if sreg:
				for x in sreg:
					status=x['studentregistrations_status']
					if status!='Approved':
						raise Exception()
				grade=Grades.objects.update_or_create(studentid=student,courseid=course,course_status=coursestatus,course_grade=coursegrade,grade_approvedby=user)
				messages.success(request,"Grade record added!")
			else:
				raise IndexError()
		except ValueError as e:
			messages.error(request,"Please enter correct student id and course id to add grade!")
		except IntegrityError as e:
			messages.error(request,"Grade already exists!")
		except Exception as e:
			messages.error(request,"Student registration for this course is not approved!")
		except IndexError as e:
			messages.error(request,"This course is not yet started by student!")
		return HttpResponseRedirect('/users')
	else :
		return HttpResponseRedirect('/users')


def setdate():
	currentDate = dt.today().strftime('%Y-%m-%d')
	return currentDate
		
class CourseListView(View):
	model=Courseregistrations
	template_name="users/register.html"
			
	def get(self, request, *args, **kwargs):
		try:
			context={}
			###### OMR query
			#queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
			cursor = connection.cursor()
			cursor.execute('''select cs.courseregistrations_id,c.course_id,c.course_name,c.course_credits,f.faculty_id,f.faculty_name from IIITS.CourseRegistrations cs join IIITS.Course c on c.course_id = cs.courseRegistrations_cid  join IIITS.Faculty f on f.Faculty_id = cs.courseRegistrations_fid ''')
			vals = cursor.fetchall()
			queryvals=[]
			print(vals[0])
			for x in vals:
				queryvals.append({"courseregistrations_id":x[0],"course_id":x[1],"course_name":x[2],"course_credits":x[3],"faculty_id":x[4],"faculty_name":x[5]})
			#print(queryvals)
			myname=request.user
			print(myname)
			student=Student.objects.values('student_roll_no','student_first_name','student_last_name','student_cur_year','student_curr_sem','student_reg_year').filter(student_email=myname)
			policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
			total_policy=len(RegistrationPolicy.objects.all())
			context['policy']=policy
			context['total_policy']=total_policy
			context['queryvals']=queryvals
			context['total_reglist']=len(queryvals)
			for i in student:
				fname = i['student_first_name']			
				lname = i['student_last_name']
				name = fname+" "+lname
				context['name']=name
				context['student_roll_no']=i['student_roll_no']
				context['student_cur_year']=i['student_cur_year']
				context['student_cur_sem']=i['student_curr_sem']
				context['student_reg_year']=i['student_reg_year']
			student_roll = context['student_roll_no']
			
			#OMR query
			#grades = Grades.objects.filter(studentid=student_roll,course_status='Completed').select_related('courseid').values('courseid__course_type','courseid__course_name','course_status','courseid__course_credits')
			cstatus="Completed"
			
			cursor = connection.cursor()
			cursor.execute('''select c.course_type,c.course_name,g.course_status,c.course_credits from IIITS.Grades g join IIITS.Course c on g.courseid=c.course_id where g.course_status= %s and g.studentid=%s ''',[cstatus,student_roll])
			vals = cursor.fetchall()
			grades=[]
			print(vals[0])
			for x in vals:
				grades.append({"course_type":x[0],"course_name":x[1],"course_status":x[2],"course_credits":x[3]})

			context['grades']=grades
			context['total_grades']=len(grades)
			# OMR query
			#mypolicy=RegistrationPolicy.objects.filter(regPolicy_year=context['student_reg_year']).values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
			
			cursor = connection.cursor()
			cursor.execute('''select r.regPolicy_Id,r.regPolicy_coursetype,r.regPolicy_credits,r.regPolicy_year from IIITS.registrationPolicy r where r.regPolicy_year= %s ''',[context['student_reg_year']])
			vals = cursor.fetchall()
			mypolicy=[]
			#print(vals[0])
			for x in vals:
				mypolicy.append({"regPolicy_Id":x[0],"regPolicy_coursetype":x[1],"regPolicy_credits":x[2],"regPolicy_year":x[3]})	
			
			todo=[]
			k=0
			balance=0
			total=0
			for y in mypolicy:
				for x in grades:
					if y['regPolicy_coursetype'] == x['course_type']:
						total = total + x['course_credits']
				balance = y['regPolicy_credits']-total			
				todo.append({'course_type':y['regPolicy_coursetype'],'total_credits':balance})
				k=k+1
				balance=0
				total=0						
			print(todo)	
			context['todo']=todo
			context['total_todo']=k
		except Exception as e:
			messages.error(request,repr(e))			
		return render(request, self.template_name,context)
			
	def post(self, request, *args, **kwargs):
		if 'saveCourseBtn' in request.POST:
			try:
				courseregistrations_id = request.POST.getlist('saveCourse')
				myname = request.POST.getlist('saveCourseBtn')
				email=request.user
				option=request.POST.getlist('csel')
				option=list(filter(None,option))
				context={}
				student=Student.objects.values('student_roll_no','student_first_name','student_last_name','student_cur_year','student_curr_sem','student_reg_year').filter(student_email=email)
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['policy']=policy
				context['total_policy']=total_policy				
				for i in student:
					fname = i['student_first_name']			
					lname = i['student_last_name']
					name = fname+" "+lname
					context['name']=name
					context['student_roll_no']=i['student_roll_no']
					context['student_cur_year']=i['student_cur_year']
					context['student_cur_sem']=i['student_curr_sem']
					context['student_reg_year']=i['student_reg_year']
				student_roll = context['student_roll_no']
				sem=i['student_curr_sem']
				grades = Grades.objects.filter(studentid=student_roll,course_status='Completed').select_related('courseid').values('courseid__course_type','courseid__course_name','course_status','courseid__course_credits')
				context['grades']=grades
				context['total_grades']=len(grades)
				mypolicy=RegistrationPolicy.objects.filter(regPolicy_year=context['student_reg_year']).values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				todo=[]
				k=0
				balance=0
				total=0
				for y in mypolicy:
					for x in grades:
						if y['regPolicy_coursetype'] == x['courseid__course_type']:
							total = total + x['courseid__course_credits']
					balance = y['regPolicy_credits']-total			
					todo.append({'courseid__course_type':y['regPolicy_coursetype'],'total_credits':balance})
					k=k+1
					balance=0
					total=0						
				print(todo)	
				context['todo']=todo
				context['total_todo']=k
				listlen = len(courseregistrations_id)
				optlen=len(option)
				if listlen <= 0:
					raise IndexError()
				for i in range(listlen):
					student_id = CustomUser.objects.values('id').filter(username=myname[0])
					for j in student_id:
						sid = j['id']
					#print(sid)
					student_no = Student.objects.values('student_roll_no').filter(student_Id=sid)
					for s in student_no:
						student_roll = s['student_roll_no']
					#print(student_roll)
					print(courseregistrations_id[i])
					val=courseregistrations_id[i]			
					coursereg = Courseregistrations.objects.filter(courseregistrations_id=val).values('courseregistrations_cid')
					print(coursereg)
					for p in coursereg:
						courseregistrations_cid=p['courseregistrations_cid']
					print(courseregistrations_cid)
					student = get_object_or_404(Student, pk=student_roll)
					course=get_object_or_404(Course, pk=courseregistrations_cid)
					checkStatus =  Studentregistrations.objects.filter(studentregistrations_sid__in=[student_roll],studentregistrations_status='Registered').values('studentregistrations_status').annotate(status_count=Count('studentregistrations_status'))
					if checkStatus:
						for status in checkStatus:
							x = status['status_count']
						if(x > 0):
							queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
							context['queryvals']=queryvals
							messages.error(request,'Your Registration already completed!! Wait for Add/Drop Course')
					else:
						if optlen != 0:
							tablesave = Studentregistrations.objects.create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Saved',studentregistrations_auditoption=option[i],studentregistrations_semester=sem)
						else:
							tablesave = Studentregistrations.objects.create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Saved',studentregistrations_auditoption='no',studentregistrations_semester=sem)
						queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
						context['queryvals']=queryvals
						messages.success(request, 'Course record saved successfully!')
			except IntegrityError as e:
				print(e)
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				#messages.error(request,'Record already exists!! Please select another record')
				context['queryvals']=queryvals
				messages.error(request,str(e))
			except IndexError as e:
				print(e)
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				context['queryvals']=queryvals
				messages.error(request,'Please select a course to save!!')
			return render(request,self.template_name,context)
		elif 'submitCourseBtn' in request.POST:
			try:	
				print("To submit course list")
				context={}
				courseregistrations_id = request.POST.getlist('saveCourse')
				myname = request.POST.getlist('submitCourseBtn')
				option=request.POST.getlist('csel')
				option=list(filter(None,option))
				listlen = len(courseregistrations_id)
				optlen=len(option)
				email=request.user
				student=Student.objects.values('student_roll_no','student_first_name','student_last_name','student_cur_year','student_curr_sem','student_reg_year').filter(student_email=email)
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['policy']=policy
				context['total_policy']=total_policy
				for i in student:
					fname = i['student_first_name']			
					lname = i['student_last_name']
					name = fname+" "+lname
					context['name']=name
					context['student_roll_no']=i['student_roll_no']					
					context['student_cur_year']=i['student_cur_year']
					context['student_cur_sem']=i['student_curr_sem']
					context['student_reg_year']=i['student_reg_year']
				student_roll = context['student_roll_no']
				sem=context['student_cur_sem']
				grades = Grades.objects.filter(studentid=student_roll,course_status='Completed').select_related('courseid').values('courseid__course_type','courseid__course_name','course_status','courseid__course_credits')
				context['grades']=grades
				context['total_grades']=len(grades)
				mypolicy=RegistrationPolicy.objects.filter(regPolicy_year=context['student_reg_year']).values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				todo=[]
				k=0
				balance=0
				total=0
				for y in mypolicy:
					for x in grades:
						if y['regPolicy_coursetype'] == x['courseid__course_type']:
							total = total + x['courseid__course_credits']
					balance = y['regPolicy_credits']-total			
					todo.append({'courseid__course_type':y['regPolicy_coursetype'],'total_credits':balance})
					k=k+1
					balance=0
					total=0						
				#print(todo)
				context['todo']=todo
				context['total_todo']=k
				student_id = CustomUser.objects.values('id').filter(username=myname[0])
				for j in student_id:
					sid = j['id']
				student_no = Student.objects.values('student_roll_no').filter(student_Id=sid)
				for s in student_no:
					student_roll = s['student_roll_no']
				checkStatus = Studentregistrations.objects.filter(studentregistrations_sid__in=[student_roll],studentregistrations_status='Registered').values('studentregistrations_status').annotate(status_count=Count('studentregistrations_status'))
				if checkStatus:
					for status in checkStatus:
						x = status['status_count']
					if(x > 0):
						queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
						context['queryvals']=queryvals
						messages.error(request,'Your Registration already completed!! Wait for Add/Drop Course')
				else:
					if listlen <= 0:
						raise IndexError()
					else:
						for i in range(listlen):
							coursereg = Courseregistrations.objects.filter(courseregistrations_id=courseregistrations_id[i]).values('courseregistrations_cid')
							for p in coursereg:
								courseregistrations_cid=p['courseregistrations_cid']
							student = get_object_or_404(Student, pk=student_roll)
							course = get_object_or_404(Course, pk=courseregistrations_cid)
							if optlen != 0:
								tablesave= Studentregistrations.objects.update_or_create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Registered',studentregistrations_auditoption=option[i],studentregistrations_semester=sem)
							else:
								tablesave= Studentregistrations.objects.update_or_create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Registered',studentregistrations_auditoption='no',studentregistrations_semester=sem)
							tablesave = Studentregistrations.objects.all().update(studentregistrations_status='Registered')
							queryvals =  Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
							context['queryvals']=queryvals
							messages.success(request,'Registration of courses completed! Wait for Add/Drop course phase for further updates')
			except IntegrityError as e:
				print(e.message)
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				context['queryvals']=queryvals
				messages.error(request,'Record already exists! Choose another course and submit')
			except IndexError as e:
				print(e)
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				context['queryvals']=queryvals
				messages.error(request,repr(e)+'Please select a course and submit!!')
			except Exception as e:
				print(e)
			return render(request,self.template_name,context)					
		
	def coursedetails(request,course_id,val):
		cursor = connection.cursor()
		#cursor.execute('''SELECT course_id,course_name,course_credits FROM IIITS.Course WHERE `course_id` = %s ''',[course_id])
		cursor.execute('''select c.course_id,c.course_name,c.course_credits,f.faculty_name from IIITS.CourseRegistrations cs join IIITS.Course c on c.course_id = cs.courseRegistrations_cid  join IIITS.Faculty f on f.Faculty_id = cs.courseRegistrations_fid where cs.courseRegistrations_cid = %s and cs.courseRegistrations_fid = %s ''',[course_id,val])
		vals = cursor.fetchall()
		queryvals=[]
		print(vals[0])
		for x in vals:
			queryvals.append({"course_id":x[0],"course_name":x[1],"course_credits":x[2],"faculty_name":x[3]})
		return render(request,"users/coursedetails.html", {'queryvals':queryvals})
	

class StudentCourseListView(View):
	model=Studentregistrations
	template_name="users/studenthome.html"
	context_object_name = 'clist'
		
	def get(self, request, *args, **kwargs):
		try:
			context={}
			queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
			course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
			total_courses=len(Course.objects.all())
			faculty = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
			total_faculty=len(Faculty.objects.all())
			context['course']=course
			context['total_courses']=total_courses
			context['faculty']=faculty
			context['total_faculty']=total_faculty
			context['queryvals']=queryvals
			context['total_reglist']=len(queryvals)
			myname=request.user
			date_format = '%Y-%m-%d'
			today=setdate()
			today=dt.strptime(today,date_format).date()
			student=Student.objects.values('student_roll_no','student_first_name','student_last_name','student_cur_year','student_curr_sem','student_reg_year').filter(student_email=myname)
			for i in student:
				fname = i['student_first_name']			
				lname = i['student_last_name']
				name = fname+" "+lname
				context['name']=name
				context['student_roll_no']=i['student_roll_no']
				context['student_cur_year']=i['student_cur_year']
				context['student_cur_sem']=i['student_curr_sem']
				context['student_reg_year']=i['student_reg_year']
			student_roll = context['student_roll_no']
			coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
			if coursevals:
				context['coursevals']=coursevals
				context['total_reglist']=len(coursevals)	
				getdates = Courseregistrations.objects.filter(courseregistrations_isactive=True).values_list('courseregistrations_updatedate','courseregistrations_finaldate')		
				if getdates:
					for s in getdates:
						udate=s[0]
						fdate=s[1]
						break
					if today < udate or today > fdate:
						enable=False
					else:
						enable=True
					context['enable']=enable
			total_credits=0
			grades = Grades.objects.filter(studentid=student_roll,course_status='Completed').select_related('courseid').values('courseid__course_type','course_status','course_grade','courseid__course_name','courseid__course_credits')
			context['grades']=grades
			for g in grades:
				total_credits=total_credits + g['courseid__course_credits']			
			context['total_grades']=len(grades)	
			context['total_credits']=total_credits
		except Exception as e:
			messages.error(request,repr(e))
		return render(request, self.template_name,context)
	
	def post(self, request, *args, **kwargs):
		if 'delCourseBtn' in request.POST:
			try:
				cid = request.POST.getlist('delCourse')
				uid = request.user
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
				course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				faculty = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				context={}
				context['queryvals']=queryvals
				context['course']=course
				context['total_courses']=total_courses
				context['faculty']=faculty
				context['total_faculty']=total_faculty
				context['coursevals']=coursevals
				context['total_reglist']=len(coursevals)
				getdates = Courseregistrations.objects.filter(courseregistrations_isactive=True).values_list('courseregistrations_updatedate','courseregistrations_finaldate')
				if getdates:
					for s in getdates:
						udate=s[0]
						fdate=s[1]
						break
				student=Student.objects.values('student_roll_no').filter(student_email=uid)
				for s in student:
					sid = s['student_roll_no']
				if len(cid) <= 0:
					raise IndexError()				
				for i in range(len(cid)):
					regrecord = Studentregistrations.objects.filter(studentregistrations_sid=sid,studentregistrations_cid=cid[i]).values('studentregistrations_status')
					for p in regrecord:
						status = p['studentregistrations_status']
					print(status)
					if status=='Saved':
						delrecord = Studentregistrations.objects.filter(studentregistrations_sid=sid,studentregistrations_cid=cid[i]).delete()
						queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
						context['queryvals']=queryvals
						context['total_reglist']=len(coursevals)
					#messages.success(request,"Selected courses deleted from registration list!")
					else:
						print("Do not delete")
						messages.error(request,'Data already submitted to review and cannot be deleted!!')				
				if getdates:
					if today < udate and today > fdate:
						enable=False
					else:
						enable=True
						context['enable']=enable
						context['total_reglist']=len(coursevals)
			except IndexError as e:
				queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
				context['queryvals']=queryvals
				context['total_reglist']=len(coursevals)
				messages.error(request,"Please select a record to delete!!")
			except Exception as e:
				queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
				context['queryvals']=queryvals
				context['total_reglist']=len(coursevals)
				messages.error(request,repr(e))
			return render(request, self.template_name,context)
		elif 'addCourseBtn' in request.POST:
			try:
				ctype = request.POST.get('ctype')
				cname = request.POST.get('cname')
				option = request.POST.get('csel')
				email=request.user
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
				course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				faculty = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				caoursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				context={}
				context['queryvals']=queryvals
				context['course']=course
				context['total_courses']=total_courses
				context['faculty']=faculty
				context['total_faculty']=total_faculty
				context['coursevals']=coursevals
				context['total_reglist']=len(coursevals)
				print(ctype)
				print(cname)
				print(option)
				print(email)
				student_val=Student.objects.values('student_roll_no').filter(student_email=email)
				print(student_val)		
				for x in student_val:
					student_roll=x['student_roll_no']
				print(student_roll)
				getreg = Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('course_registrations_cid').prefetch_related('courseregistrations_fid').values_list('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year','courseregistrations_cid','courseregistrations_cid__course_type','courseregistrations_cid__course_name')
				print(getreg)
				if getreg:
					for s in getreg:
						print(s[7])
						print(s[8])
						if ctype == s[7] and cname == s[8]:
							sdate=str(s[0])
							edate=str(s[1])
							udate=str(s[2])
							fdate=str(s[3])
							csem=str(s[4])
							cyear=str(s[5])
							cid=str(s[6])
							break
				print(sdate)
				print(edate)
				print(udate)
				print(fdate)
				print(csem)
				print(cyear)
				print(cid)
				course=get_object_or_404(Course,pk=cid)
				student=get_object_or_404(Student,pk=student_roll)
				getrec = Studentregistrations.objects.filter(studentregistrations_cid=cid,studentregistrations_sid=student_roll).values('studentregistrations_id')
				if getrec:
					messages.error(request,"Record already exists!")
				else:
					tablesave = Studentregistrations.objects.create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Saved',studentregistrations_auditoption=option)
					messages.success(request,"Record added to registration list")
					queryvals = Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid','studentregistrations_auditoption')
					context['queryvals']=queryvals
					context['total_reglist']=len(coursevals)
				getdates = Courseregistrations.objects.filter(courseregistrations_isactive=True).values_list('courseregistrations_updatedate','courseregistrations_finaldate')
				if getdates:
					for s in getdates:
						udate=s[0]
						fdate=s[1]
						break
				if getdates:
					if today < udate and today > fdate:
						enable=False
					else:
						enable=True
						context['enable']=enable
			except Exception as e:
				messages.error(request,repr(e))
			return render(request, self.template_name,context)				
				
class RegCourseListView(View):
	model=Courseregistrations
	template_name="users/courselist.html"
	def get(self, request, *args, **kwargs):
		context={}
		course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
		total_courses=len(Course.objects.all())
		faculty = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
		total_faculty=len(Faculty.objects.all())
		policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
		total_policy=len(RegistrationPolicy.objects.all())		
		date_format = '%Y-%m-%d'
		today=setdate()
		today=dt.strptime(today,date_format).date()
		coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
		if coursevals:
			regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
			if regvals:
				for r in regvals:
					context['startdate']=r['courseregistrations_startdate']
					context['enddate']=r['courseregistrations_enddate']
					context['updatedate']=r['courseregistrations_updatedate']
					context['finaldate']=r['courseregistrations_finaldate']
					context['sem']=r['courseregistrations_semester']
					if context['sem'] == 'Spring':
						context['Spring']=True
					elif context['sem'] == 'Fall':
						context['Fall']=True
					context['year']=r['courseregistrations_year']
				context['enable']=True			
			if today > context['finaldate']:
				print("reg date is over")
				context['enable']=False
		else:
			day=setdate()
			courseids =Courseregistrations.objects.filter(courseregistrations_finaldate__lt=day)
			if courseids:
				context['enable']=False
			else:
				context['enable']=True
		context['course']=course
		context['total_courses']=total_courses
		context['faculty']=faculty
		context['policy']=policy		
		context['total_faculty']=total_faculty
		context['total_policy']=total_policy
		context['coursevals']=coursevals
		context['total_reglist']=len(coursevals)			
		return render(request, self.template_name,context)
		
	def post(self, request, *args, **kwargs):
		if 'changeBtn' in request.POST:
			try:
				context={}
				start_date = request.POST.getlist('sdate')
				end_date=request.POST.getlist('edate')
				update_date=request.POST.getlist('udate')
				final_date=request.POST.getlist('fdate')
				sem=request.POST.getlist('sem')
				year=request.POST.getlist('year')
				course_id = request.POST.getlist('saveCourse')
				course_offered_to = request.POST.getlist('csel')
				size = request.POST.getlist('max')
				faculty = request.POST.getlist('fid')
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				context['course']=courselist
				total_courses=len(Course.objects.all())
				context['total_courses']=total_courses
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				context['faculty']=facultylist
				total_faculty=len(Faculty.objects.all())
				context['total_faculty']=total_faculty
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['policy']=policy				
				context['total_policy']=total_policy
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				if coursevals:
					context['coursevals']=coursevals
					context['total_reglist']=len(coursevals)
					regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if regvals:
						for r in regvals:
							context['startdate']=r['courseregistrations_startdate']
							context['enddate']=r['courseregistrations_enddate']
							context['updatedate']=r['courseregistrations_updatedate']
							context['finaldate']=r['courseregistrations_finaldate']
							context['sem']=r['courseregistrations_semester']
							if context['sem'] == 'Spring':
								context['Spring']=True
							elif context['sem'] == 'Fall':
								context['Fall']=True
							context['year']=r['courseregistrations_year']			
						context['enable']=True
						if today > context['finaldate']:
							print("reg date is over")
							context['enable']=False
							raise ValueError('Registration Final Date is earlier than today')
				else: 
					day=setdate()
					courseids =Courseregistrations.objects.filter(courseregistrations_finaldate__lt=day)
					if courseids:
						context['enable']=False
					else:
						context['enable']=True
					
				db_start_date=dt.strptime(start_date[0], date_format).date()
				print(db_start_date)
				db_end_date=dt.strptime(end_date[0], date_format).date()
				print(db_end_date)
				db_update_date=dt.strptime(update_date[0], date_format).date()
				print(db_update_date)
				db_final_date=dt.strptime(final_date[0], date_format).date()
				print(db_final_date)
				print(today)
				if today > db_start_date:
					raise ValueError('Start date is earlier than today')
				if today > db_end_date:
					raise ValueError('End date is earlier than today')
				if today > db_update_date:
					raise ValueError('Update date is earlier than today')	
				if today > db_final_date:
					raise ValueError('Final date is earlier than today')
				if db_start_date > db_end_date:
					raise ValueError('Start date is later than end date')
				if db_update_date < db_start_date:
					raise ValueError('Update data is earlier than start date')
				if db_final_date < db_update_date:
					raise ValueError('Final date is earlier than update date')
				getreg =Courseregistrations.objects.filter(courseregistrations_isactive=True).update(courseregistrations_startdate=db_start_date,courseregistrations_enddate=db_end_date,courseregistrations_updatedate=db_update_date,courseregistrations_finaldate=db_final_date,courseregistrations_semester=sem[0],courseregistrations_year=year[0])
				if getreg > 0:
					messages.success(request,"Schedule updated for current registration!")
					regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if regvals:
						for r in regvals:
							context['startdate']=r['courseregistrations_startdate']
							context['enddate']=r['courseregistrations_enddate']
							context['updatedate']=r['courseregistrations_updatedate']
							context['finaldate']=r['courseregistrations_finaldate']
							context['sem']=r['courseregistrations_semester']
							if context['sem'] == 'Spring':
								context['Spring']=True
							elif context['sem'] == 'Fall':
								context['Fall']=True
							context['year']=r['courseregistrations_year']
						context['enable']=True
					else:
						context['enable']=False					
				else:
					messages.error(request,"No matching records to update schedule for current registration!")
			except ValueError as e:
				messages.error(request,repr(e))
			return render(request, self.template_name,context)
		elif 'saveCourseBtn' in request.POST:
			try:
				context={}
				start_date = request.POST.getlist('sdate')
				end_date=request.POST.getlist('edate')
				update_date=request.POST.getlist('udate')
				final_date=request.POST.getlist('fdate')
				sem=request.POST.getlist('sem')
				year=request.POST.getlist('year')
				course_id = request.POST.getlist('saveCourse')
				course_offered_to = request.POST.getlist('csel')
				size = request.POST.getlist('max')
				faculty = request.POST.getlist('fid')
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				size=list(filter(None,size))
				faculty=list(filter(None,faculty))
				listlen = len(faculty)
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['course']=courselist
				context['faculty']=facultylist
				context['policy']=policy
				context['total_courses']=total_courses
				context['total_faculty']=total_faculty
				context['total_policy']=total_policy
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				context['coursevals']=coursevals
				context['total_reglist']=len(coursevals)
				context['enable']=True
				if listlen<=0 or not start_date[0] or not end_date[0] or not update_date[0] or not final_date[0]:
					raise IndexError()
				db_start_date=dt.strptime(start_date[0], date_format).date()
				#print(db_start_date)
				if today > db_start_date:
					raise ValueError('Start date is earlier than today')
				db_end_date=dt.strptime(end_date[0], date_format).date()
				if today > db_end_date:
					raise ValueError('End date is earlier than today')
				#print(db_end_date)
				db_update_date=dt.strptime(update_date[0], date_format).date()
				if today > db_update_date:
					raise ValueError('Update date is earlier than today')
				#print(db_update_date)
				db_final_date=dt.strptime(final_date[0], date_format).date()
				#print(db_final_date)					
				if today > db_final_date:
					raise ValueError('Final date is earlier than today')
				if db_start_date > db_end_date:
					raise ValueError('Start date is later than end date')
				if db_update_date < db_start_date:
					raise ValueError('Update data is earlier than start date')
				if db_final_date < db_update_date:
					raise ValueError('Final date is earlier than update date')									
				regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
				if regvals:
					for r in regvals:
						context['startdate']=r['courseregistrations_startdate']
						context['enddate']=r['courseregistrations_enddate']
						context['updatedate']=r['courseregistrations_updatedate']
						context['finaldate']=r['courseregistrations_finaldate']
						context['sem']=r['courseregistrations_semester']
						if context['sem'] == 'Spring':
							context['Spring']=True
						elif context['sem'] == 'Fall':
							context['Fall']=True
						context['year']=r['courseregistrations_year']			
					context['enable']=True	
					
					if context['startdate']!=db_start_date:
						sdate=str(context['startdate'])
						raise ValueError('Original Start Date is '+db_start_date+' Click on change Schedule to update the details!')
					elif context['enddate']!=db_end_date:
						raise ValueError('Original End Date is '+db_end_date+' Click on change Schedule to update the details!')
					elif context['updatedate']!=db_update_date:
						raise ValueError('Original Update Date is '+db_update_date+'  Click on change Schedule to update the details!')
					elif context['finaldate']!=db_final_date:
						raise ValueError('Original Final Date is '+db_final_date+'  Click on change Schedule to update the details!')
					elif context['sem']!=sem[0]:
						raise ValueError('Earlier Semester is '+context['sem']+'  Click on change Schedule to update the details!')
					elif context['year']!=year[0]:
						raise ValueError('Earlier year is '+context['year']+'  Click on change Schedule to update the details!')
					if today > context['finaldate']:
						context['enable']=False
						raise ValueError('Registration Final Date is earlier than today')
				else:
					context['enable']=True
				for i in range(listlen):
					courseinfo = get_object_or_404(Course, pk=int(course_id[i]))
					f=get_object_or_404(Faculty,pk=int(faculty[i]))
					tablesave =Courseregistrations.objects.update_or_create(courseregistrations_cid=courseinfo,courseregistrations_fid=f,courseregistrations_startdate=db_start_date,courseregistrations_enddate=db_end_date,courseregistrations_updatedate=db_update_date,courseregistrations_finaldate=db_final_date,courseregistrations_semester=sem[0],courseregistrations_year=year[0],courseregistrations_offeredto=course_offered_to[i],courseregistrations_classsize=size[i],courseregistrations_isactive=True)
					messages.success(request,"Selected courses added to registration list!")
					#detailed added to reg course list after save record
				if tablesave:
					coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
					context['coursevals']=coursevals
					context['total_reglist']=len(coursevals)								
			except IndexError as e:
				print("Please select a record and save!!") 
				messages.error(request,"Please select a record and fill all details to save the course!")
			except ValueError as e:
				messages.error(request,repr(e))
			except IntegrityError as e:
				messages.error(request,repr(e))			
			return render(request, self.template_name,context)
		elif 'addPolicyBtn' in request.POST:
			try:
				context={}
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				ctype=request.POST.get('ctype')
				credits=request.POST.get('pcredits')
				year=request.POST.get('pyear')
				name=request.user
				user=CustomUser.objects.values('id').filter(email=name)
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				for x in user:
					uid=x['id']
				user=get_object_or_404(CustomUser,pk=uid)				
				print(user)
				regpolicy = RegistrationPolicy.objects.create(regPolicy_coursetype=ctype,regPolicy_credits=credits,regPolicy_year=year,regPolicy_updateddby=user)
				if regpolicy:
					messages.success(request,"Created new policy!")			
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['course']=courselist
				context['faculty']=facultylist
				context['policy']=policy
				context['total_courses']=total_courses
				context['total_faculty']=total_faculty
				context['total_policy']=total_policy
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				if coursevals:
					context['coursevals']=coursevals
					context['total_reglist']=len(coursevals)
					regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if regvals:
						for r in regvals:
							context['startdate']=r['courseregistrations_startdate']
							context['enddate']=r['courseregistrations_enddate']
							context['updatedate']=r['courseregistrations_updatedate']
							context['finaldate']=r['courseregistrations_finaldate']
							context['sem']=r['courseregistrations_semester']
							if context['sem'] == 'Spring':
								context['Spring']=True
							elif context['sem'] == 'Fall':
								context['Fall']=True
							context['year']=r['courseregistrations_year']			
						context['enable']=True
						if today > context['finaldate']:
							context['enable']=False
					else:
						context['enable']=True				
			except ValueError as e:
				messages.error(request,repr(e)+'Add all details to add policy details!')
			return render(request, self.template_name,context)
		elif 'changePolicyBtn' in request.POST:
			try:
			    context={}
			    courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
			    total_courses=len(Course.objects.all())
			    facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
			    total_faculty=len(Faculty.objects.all())
			    policy=RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
			    total_policy=len(RegistrationPolicy.objects.all())
			    date_format = '%Y-%m-%d'
			    today=setdate()
			    today=dt.strptime(today,date_format).date()
			    context['course']=courselist
			    context['faculty']=facultylist
			    context['policy']=policy
			    context['total_courses']=total_courses
			    context['total_faculty']=total_faculty
			    context['total_policy']=total_policy
			    coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
			    if coursevals:
			    	context['coursevals']=coursevals
			    	context['total_reglist']=len(coursevals)
			    	regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
			    	if regvals:
			    		for r in regvals:
			    			context['startdate']=r['courseregistrations_startdate']
			    			context['enddate']=r['courseregistrations_enddate']
			    			context['updatedate']=r['courseregistrations_updatedate']
			    			context['finaldate']=r['courseregistrations_finaldate']
			    			context['sem']=r['courseregistrations_semester']
			    			if context['sem'] == 'Spring':
			    				context['Spring']=True
			    			elif context['sem'] == 'Fall':
			    				context['Fall']=True
			    			context['year']=r['courseregistrations_year']
			    		context['enable']=True
			    		if today > context['finaldate']:
			    			context['enable']=False
			    	else:
			    		context['enable']=True
			    ctype=request.POST.getlist('ctype')
			    credits=request.POST.getlist('credits')
			    year=request.POST.getlist('year')
			    ids=request.POST.getlist('savePolicy')
			    pids=request.POST.getlist('pid')
			    name=request.user
			    user=CustomUser.objects.values('id').filter(email=name)
			    for x in user:
			    	uid=x['id']
			    user=get_object_or_404(CustomUser,pk=uid)
			    l1=len(ctype)
			    l2=len(credits)
			    l3=len(year)
			    l4=len(ids)
			    l5=len(pids)
			    if l1==0 or l2==0 or l3==0 or l4==0:
			    	raise ValueError()
			    if l1!=l2 or l1!=l3 or l2!=l3:
			    	raise ValueError()
			    for i in range(l4):
			    	print(ids[i])
			    	for j in range(l5):
			    		if ids[i]==pids[j]:
			    			break
			    	if not ctype[j] or not credits[j] or not year[j]:
			    		raise ValueError()
			    	policy=get_object_or_404(RegistrationPolicy,pk=ids[i])
			    	regVal =RegistrationPolicy.objects.filter(pk=ids[i]).update(regPolicy_coursetype=ctype[j],regPolicy_credits=credits[j],regPolicy_year=year[j])
			    	if regVal:
			    		messages.success(request,"Updated policy details!")
			    policy=RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
			    total_policy=len(RegistrationPolicy.objects.all())		
			except ValueError as e:
				messages.error(request,repr(e)+'Add all details to change policy details!')
			return render(request, self.template_name,context)
		elif 'delCourseBtn' in request.POST:
			try:
				context={}
				start_date = request.POST.getlist('sdate')
				end_date=request.POST.getlist('edate')
				update_date=request.POST.getlist('udate')
				final_date=request.POST.getlist('fdate')
				sem=request.POST.getlist('sem')
				year=request.POST.getlist('year')
				course_id = request.POST.getlist('saveCourse')
				course_offered_to = request.POST.getlist('csel')
				size = request.POST.getlist('max')
				faculty = request.POST.getlist('fid')
				size=list(filter(None,size))
				faculty=list(filter(None,faculty))
				listlen = len(faculty)
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())
				context['course']=courselist
				context['faculty']=facultylist
				context['policy']=policy
				context['total_courses']=total_courses
				context['total_faculty']=total_faculty
				context['total_policy']=total_policy			
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				context['coursevals']=coursevals
				context['total_reglist']=len(coursevals)
				context['enable']=True
				if listlen<=0 or not start_date[0] or not end_date[0] or not update_date[0] or not final_date[0]:
					raise IndexError()
				regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
				if regvals:
					for r in regvals:
						context['startdate']=r['courseregistrations_startdate']
						context['enddate']=r['courseregistrations_enddate']
						context['updatedate']=r['courseregistrations_updatedate']
						context['finaldate']=r['courseregistrations_finaldate']
						context['sem']=r['courseregistrations_semester']
						if context['sem'] == 'Spring':
							context['Spring']=True
						elif context['sem'] == 'Fall':
							context['Fall']=True
						context['year']=r['courseregistrations_year']			
					context['enable']=True
					if today > context['finaldate']:
						print("reg date is over")
						context['enable']=False
						raise ValueError('Registration Final Date is earlier than today')							
					else:
						for i in range(listlen):
							courseinfo = get_object_or_404(Course, pk=int(course_id[i]))
							f=get_object_or_404(Faculty,pk=int(faculty[i]))
							tablesave=								Courseregistrations.objects.filter(courseregistrations_cid=courseinfo,courseregistrations_fid=f,courseregistrations_isactive=True).delete()
						messages.success(request,"Selected courses deleted from registration list!")
						if tablesave:
							coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
							context['coursevals']=coursevals
							context['total_reglist']=len(coursevals)
							#detailed added to reg course list after save record
				else:
					context['enable']=True							
			except IndexError as e:
				print("Please select a record to delete!!") 
				messages.error(request,"Please select a record  to delete the course!")
			except ValueError as e:
				messages.error(request,repr(e))
			except IntegrityError as e:
				messages.error(request,repr(e))			
			return render(request, self.template_name,context)
		elif 'closeRegBtn' in request.POST:
			try:
				context={}
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())				
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				context['course']=courselist
				context['faculty']=facultylist
				context['policy']=policy
				context['total_courses']=total_courses
				context['total_faculty']=total_faculty
				context['total_policy']=total_policy
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				if coursevals:
					context['coursevals']=coursevals
					context['total_reglist']=len(coursevals)
					regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if regvals:
						for r in regvals:
							context['startdate']=r['courseregistrations_startdate']
							context['enddate']=r['courseregistrations_enddate']
							context['updatedate']=r['courseregistrations_updatedate']
							context['finaldate']=r['courseregistrations_finaldate']
							context['sem']=r['courseregistrations_semester']
							if context['sem'] == 'Spring':
								context['Spring']=True
							elif context['sem'] == 'Fall':
								context['Fall']=True
							context['year']=r['courseregistrations_year']			
						context['enable']=True
						if today > context['finaldate']:
							context['enable']=False
							raise ValueError('Registration Final Date is earlier than today')
					prevday=today-timedelta(days=1)
					getreg=Courseregistrations.objects.filter(courseregistrations_isactive=True).update(courseregistrations_isactive=False,courseregistrations_finaldate=prevday)
					if getreg:
						messages.success(request,"Course registration closed!")
						context['enable']=False
						coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
						context['coursevals']=coursevals
						context['total_reglist']=len(coursevals)
			except Exception as e:
				print(e)
				messages.error(request,repr(e)+"Registration Closure failed!")			
			return render(request, self.template_name,context)
		elif 'addPrerequisiteBtn' in request.POST:
			try:
				print("Prerequisite")
				context={}
				courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
				total_courses=len(Course.objects.all())
				facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
				total_faculty=len(Faculty.objects.all())
				policy = RegistrationPolicy.objects.all().values('regPolicy_Id','regPolicy_coursetype','regPolicy_credits','regPolicy_year')
				total_policy=len(RegistrationPolicy.objects.all())				
				date_format = '%Y-%m-%d'
				today=setdate()
				today=dt.strptime(today,date_format).date()
				context['course']=courselist
				context['faculty']=facultylist
				context['policy']=policy
				context['total_courses']=total_courses
				context['total_faculty']=total_faculty
				context['total_policy']=total_policy
				coursevals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id','courseregistrations_offeredto','courseregistrations_classsize')
				if coursevals:
					context['coursevals']=coursevals
					context['total_reglist']=len(coursevals)
					regvals = Courseregistrations.objects.filter(courseregistrations_isactive=True).values('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if regvals:
						for r in regvals:
							context['startdate']=r['courseregistrations_startdate']
							context['enddate']=r['courseregistrations_enddate']
							context['updatedate']=r['courseregistrations_updatedate']
							context['finaldate']=r['courseregistrations_finaldate']
							context['sem']=r['courseregistrations_semester']
							if context['sem'] == 'Spring':
								context['Spring']=True
							elif context['sem'] == 'Fall':
								context['Fall']=True
							context['year']=r['courseregistrations_year']			
						context['enable']=True
						if today > context['finaldate']:
							context['enable']=False
							raise ValueError('Registration Final Date is earlier than today')
				else:
					content['enable']=True
				currentcourse = request.POST.get("cname")
				prereqcourse = request.POST.get("pname")
				mingrade = request.POST.get("mingrade")
				comments = request.POST.get("comments")
				myname = request.user
				Currentcid = Course.objects.filter(course_name=currentcourse).values('course_id','course_hasprereqs')
				prereqcourse = Course.objects.filter(course_name=prereqcourse).values('course_id')
				
				for c in Currentcid:
					current_cid = c['course_id']
					course_haspreq = c['course_hasprereqs'] 
				for p in prereqcourse:
					prereqid = p['course_id']
				if course_haspreq == 1:
					print(course_haspreq)
				else:
					raise IndexError()
				user_id = CustomUser.objects.filter(email=myname).values('id')
				for x in user_id:
					uid=x['id']
				currentcourse=get_object_or_404(Course,pk=current_cid)
				prereqcourse=get_object_or_404(Course,pk=prereqid)
				user=get_object_or_404(CustomUser,pk=uid)
				tablesave = CoursePreReqs.objects.update_or_create(prereq_currentcourse=currentcourse,prereq_courseid=prereqcourse,prereq_min_grade=mingrade,prereq_descr=comments,prereq_last_accessby=user)
				if tablesave:
					messages.success(request,"Prerequisite information updated!")
				else:
					raise Exception()
			except IntegrityError as e:
				messages.error(request,"Record already exists")
			except IndexError as e:
				messages.error(request,"Selected course has no prereqisites!")	
			except Exception as e:	
				messages.error(request,repr(e))	
			return render(request, self.template_name,context)
				
