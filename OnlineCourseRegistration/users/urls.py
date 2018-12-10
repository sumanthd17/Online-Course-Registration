from django.urls import path,include
from django.conf.urls import url
from django.views.generic.base import TemplateView,RedirectView

from . import views
from  .views import CourseListView,StudentCourseListView,RegCourseListView,Login,SignUp

#

app_name = 'users'

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('login/', Login.as_view(), name='in'),
	path('login.html/', Login.as_view(), name='in'),
	path('profile.html/', TemplateView.as_view(template_name='users/profile.html'), name='profile'),
	path('add_sprofile/', views.add_sprofile, name='sprofile'),	
	path('', views.index, name='index'),
	url('^callback/(?P<token>.+)$', views.callback, name='callback'),	
	path('<int:course_id>/', views.details, name='details'),
	path('add_course/', views.add_course, name='add_course'),
	path('add_student/', views.add_student, name='add_student'),
	path('students/', views.display_students, name='display_students'),
	path('audit_course/', views.audit_course, name='audit_course'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
	path('add_grade/',views.add_grade,name='add_grade'),
	path('publish_course_registration/',views.publish_course_registrations, name='publish_course_registrations'),
	path('view_registration/',views.view_registration, name='view_registration'),
	path('faculty/', views.faculty, name='faculty'),
	path('register.html/', CourseListView.as_view(),name='RegCourseList'),
	path('<int:course_id>/special_req/', views.special_req, name='special_req'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
	path('(P<course_id>\d+)/(P<val>\d+)/', views.CourseListView.coursedetails, name='coursedetails'),
	path('coursedetails.html/',TemplateView.as_view(template_name='users/coursedetails.html'),name="coursevals"),
	path('approve_req/', views.approve_req, name='approve_req'),
	path('approve_req/<int:request_id>/special_req_res_acc/', views.special_req_res_acc, name='special_req_res_acc'),
	path('approve_req/<int:request_id>/special_req_res_dec/', views.special_req_res_dec, name='special_req_res_dec'),
	#path('studenthome.html/',TemplateView.as_view(template_name='users/studentehome.html'),name="studenthome"),
	path('studenthome.html/',StudentCourseListView.as_view(),name='MyCourseList'),
	path('courselist.html/',RegCourseListView.as_view(),name='regcourselist'),
	path('publish_reg_pdf/', views.publish_course_registrations),
	path('ClassRoaster/',views.ClassRoaster,name='ClassRoaster'),
	path('deleteReg/',views.deleteReg,name='deleteReg'),
]
