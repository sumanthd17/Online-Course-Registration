from django.urls import reverse_lazy,reverse
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count

from .models import Course,Grades, Student,Courseregistrations
from .models import *
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth import *
import requests, json
from datetime import datetime as dt
import pytz


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
		grade = Grade()
		grade.student_id = request.POST.get('user_id')
		grade.course = request.POST.get('course')
		grade.grade_point = request.POST.get('grade_point')
		grade.save()
		return HttpResponseRedirect('/users')
	else :
		return HttpResponseRedirect('/users')


def setyear():
	currentYear = dt.now().year
	return currentYear
		
class CourseListView(View):
	model=Courseregistrations
	template_name="users/register.html"
				
	def get(self, request, *args, **kwargs):
		queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_id','courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
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
			try:
				courseregistrations_id = request.POST.getlist('saveCourse')
				myname = request.POST.getlist('saveCourseBtn')
				listlen = len(courseregistrations_id)
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
					coursereg = Courseregistrations.objects.filter(courseregistrations_id=int(val)).values('courseregistrations_cid')
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
							messages.error(request,'Your Registration already completed!! Wait for Add/Drop Course')
					else:
						tablesave = Studentregistrations.objects.create(studentregistrations_cid=course, studentregistrations_sid=student,studentregistrations_status='Saved')
						queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
						messages.success(request, 'Course record saved successfully!')
			except IntegrityError as e:
				print(e)
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				#messages.error(request,'Record already exists!! Please select another record')
				messages.error(request,str(e))
			except IndexError as e:
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Please select a course to save!!')		
			return render(request,self.template_name,{'queryvals': queryvals})
		elif 'submitCourseBtn' in request.POST:
			try:
				courseregistrations_id = request.POST.getlist('saveCourse')
				myname = request.POST.getlist('submitCourseBtn')
				listlen = len(courseregistrations_id)
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
							tablesave= Studentregistrations.objects.update_or_create(studentregistrations_cid=course,studentregistrations_sid=student,studentregistrations_status='Registered')
							tablesave = Studentregistrations.objects.all().update(studentregistrations_status='Registered')
							queryvals =  Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
							messages.success(request,'Registration of courses completed! Wait for Add/Drop course phase for further updates')
			except IntegrityError as e:
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Record already exists! Choose another course and submit')
			except IndexError as e:
				queryvals =Courseregistrations.objects.filter(courseregistrations_isactive=True).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
				messages.error(request,'Please select a course and submit!!')
			except Exception as e:
				print(e)
			return render(request,self.template_name,{'queryvals': queryvals})					
		
	def coursedetails(request,course_id,val):
		print(val)
		queryvals =Courseregistrations.objects.filter(courseregistrations_cid=course_id,courseregistrations_fid=val).select_related('courseregistrations_cid').select_related('courseregistrations_fid').values('courseregistrations_cid__course_id','courseregistrations_cid__course_name','courseregistrations_cid__course_credits','courseregistrations_cid__course_type','courseregistrations_cid__course_hasprereqs','courseregistrations_fid__faculty_name','courseregistrations_fid__faculty_id')
		print(queryvals)
		return render(request,"users/coursedetails.html",{'queryvals': queryvals})
	

class StudentCourseListView(View):
	model=Studentregistrations
	template_name="users/studenthome.html"
	context_object_name = 'clist'
			
	def get(self, request, *args, **kwargs):
		queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid')
		course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
		context={}
		context['queryvals']=queryvals
		context['course']=course
		return render(request, self.template_name,context)
	
	def post(self, request, *args, **kwargs):
		if 'delCourseBtn' in request.POST:
			cid = request.POST.getlist('delCourse')
			print(cid)
			uid = request.user
			student=Student.objects.values('student_roll_no').filter(student_email=uid)
			for s in student:
				sid = s['student_roll_no']					
			for i in range(len(cid)):
				regrecord = Studentregistrations.objects.filter(studentregistrations_sid=sid,studentregistrations_cid=cid[i]).values('studentregistrations_status')
				for p in regrecord:
					status = p['studentregistrations_status']
					print(status)
					if status=='Saved':
						delrecord = Studentregistrations.objects.filter(studentregistrations_sid=sid,studentregistrations_cid=cid[i]).delete()
					#messages.success(request,"Selected courses deleted from registration list!")
					else:
						print("Do not delete")
						messages.error(request,'Data already submitted to review and cannot be deleted!!')			
			queryvals =Studentregistrations.objects.all().select_related('studentregistrations_cid').prefetch_related('studentregistrations_sid').values('studentregistrations_cid__course_id','studentregistrations_cid__course_name','studentregistrations_cid__course_credits','studentregistrations_status','studentregistrations_sid')
			course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
			context={}
			context['queryvals']=queryvals
			context['course']=course			
			return render(request, self.template_name,context)
			
				
class RegCourseListView(View):
	model=Courseregistrations
	template_name="users/courselist.html"
	context_object_name = 'clist'
			
	def get(self, request, *args, **kwargs):
		course = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
		faculty = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
		context={}
		context['course']=course
		context['faculty']=faculty
		return render(request, self.template_name,context)
		
	def post(self, request, *args, **kwargs):
		print("Form submitted")
		if 'changeBtn' in request.POST:
			print("To change dates")
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
			print(start_date)
			print(end_date)
			print(update_date)
			print(final_date)
			print(sem)
			print(year)
			date_format = '%Y-%m-%d'
			db_start_date=dt.strptime(start_date[0], date_format).date()
			print(db_start_date)
			db_end_date=dt.strptime(end_date[0], date_format).date()
			print(db_end_date)
			db_update_date=dt.strptime(update_date[0], date_format).date()
			print(db_update_date)
			db_final_date=dt.strptime(final_date[0], date_format).date()
			print(db_final_date)
			current_year=setyear()
			print(current_year)
			courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
			facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
			context={}
			context['course']=courselist
			context['faculty']=facultylist
			getreg =Courseregistrations.objects.filter(courseregistrations_isactive=True).update(courseregistrations_startdate=db_start_date,courseregistrations_enddate=db_end_date,courseregistrations_updatedate=db_update_date,courseregistrations_finaldate=db_final_date,courseregistrations_semester=sem[0],courseregistrations_year=year[0])
			if getreg > 0:
				messages.success(request,"Schedule updated for current registration!")
			else:
				messages.error(request,"No matching records to update schedule for current registration!")
		else:
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
			print(start_date)
			print(end_date)
			print(update_date)
			print(final_date)
			print(sem)
			print(year)		
			print(course_id)
			print(faculty)
			print(course_offered_to)
			size=list(filter(None,size))
			faculty=list(filter(None,faculty))
			print(faculty)
			listlen = len(faculty)
			date_format = '%Y-%m-%d'
			db_start_date=dt.strptime(start_date[0], date_format).date()
			print(db_start_date)
			db_end_date=dt.strptime(end_date[0], date_format).date()
			print(db_end_date)
			db_update_date=dt.strptime(update_date[0], date_format).date()
			print(db_update_date)
			db_final_date=dt.strptime(final_date[0], date_format).date()
			print(db_final_date)		
			try:
				if listlen <=0:
					raise IndexError()
				else:
					courselist = Course.objects.all().values('course_id','course_name','course_delivery_mode','course_type','course_credits')
					facultylist = Faculty.objects.all().values('faculty_id','faculty_name','faculty_designation')
					context={}
					context['course']=courselist
					context['faculty']=facultylist
					getreg = Courseregistrations.objects.filter(courseregistrations_isactive=True).values_list('courseregistrations_startdate','courseregistrations_enddate','courseregistrations_updatedate','courseregistrations_finaldate','courseregistrations_semester','courseregistrations_year')
					if getreg:
						for s in getreg:
							sdate=str(s[0])
							edate=str(s[1])
							udate=str(s[2])
							fdate=str(s[3])
							csem=str(s[4])
							cyear=str(s[5])
						if sdate!=start_date[0] and csem==sem[0]:
							raise ValueError('Original Start Date is '+sdate)
						elif edate!=end_date[0] and csem==sem[0]:
							raise ValueError('Original End Date is '+edate)
						elif udate!=update_date[0] and csem==sem[0]:
							raise ValueError('Original Update Date is '+udate)
						elif fdate!=final_date[0] and csem==sem[0]:
							raise ValueError('Original Final Date is '+fdate)
						elif csem!=sem[0]:
							raise ValueError('Earlier Semester is '+csem)
						elif cyear!=year[0]:
							raise ValueError('Earlier year is '+cyear)
						else:
							for i in range(listlen):
								courseinfo = get_object_or_404(Course, pk=int(course_id[i]))
								f=get_object_or_404(Faculty,pk=int(faculty[i]))
								tablesave =Courseregistrations.objects.update_or_create(courseregistrations_cid=courseinfo,courseregistrations_fid=f,courseregistrations_startdate=db_start_date,courseregistrations_enddate=db_end_date,courseregistrations_updatedate=db_update_date,courseregistrations_finaldate=db_final_date,courseregistrations_semester=sem[0],courseregistrations_year=year[0],courseregistrations_offeredto=course_offered_to[i],courseregistrations_classsize=size[i],courseregistrations_isactive=True)
								messages.success(request,"Selected courses added to registration list!")
					else:
						for i in range(listlen):
							courseinfo = get_object_or_404(Course, pk=int(course_id[i]))
							f=get_object_or_404(Faculty,pk=int(faculty[i]))
							tablesave =Courseregistrations.objects.update_or_create(courseregistrations_cid=courseinfo,courseregistrations_fid=f,courseregistrations_startdate=db_start_date,courseregistrations_enddate=db_end_date,courseregistrations_updatedate=db_update_date,courseregistrations_finaldate=db_final_date,courseregistrations_semester=sem[0],courseregistrations_year=year[0],courseregistrations_offeredto=course_offered_to[i],courseregistrations_classsize=size[i],courseregistrations_isactive=True)
							messages.success(request,"Selected courses added to registration list!")					
			except IndexError as e:
				print("Please select a record and save!!")
				messages.error(request,"Please select a record to save!")
			except ValueError as e:
				messages.error(request,repr(e)+'Click on Schedule Change to change details!')
		return render(request, self.template_name,context)
