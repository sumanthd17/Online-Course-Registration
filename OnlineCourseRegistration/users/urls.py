from django.urls import path,include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views
from  .views import CourseListView

#

app_name = 'users'

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('', views.index, name='index'),
	url('^callback/(?P<token>.+)$', views.callback, name='callback'),	
	path('<int:course_id>/', views.details, name='details'),
	path('add_course/', views.add_course, name='add_course'),
	path('add_student/', views.add_student, name='add_student'),
	path('audit_course/', views.audit_course, name='audit_course'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
	path('add_grade/',views.add_grade,name='add_grade'),
	path('publish_course_registration/',views.publish_course_registration, name='publish_course_registration'),
	path('view_registration/',views.view_registration, name='view_registration'),
	path('faculty/', views.faculty, name='faculty'),
	path('Students.html/', CourseListView.as_view(),name='MyCourseList'),
	path('<int:course_id>/special_req/', views.special_req, name='special_req'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
	path('(P<academic_course_id>\d+)/(P<val>\d+)/', views.CourseListView.coursedetails, name='coursedetails'),
	path('coursedetails.html/',TemplateView.as_view(template_name='users/coursedetails.html'),name="coursevals"),
	path('approve_req/', views.approve_req, name='approve_req'),
	path('approve_req/<int:request_id>/special_req_res_acc/', views.special_req_res_acc, name='special_req_res_acc'),
	path('approve_req/<int:request_id>/special_req_res_dec/', views.special_req_res_dec, name='special_req_res_dec'),
]
