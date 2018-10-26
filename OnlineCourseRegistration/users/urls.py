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
	path('<int:course_id>/', views.details, name='details'),
	path('add_course/', views.add_course, name='add_course'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
	path('Students.html/', CourseListView.as_view(),name='MyCourseList'),
	path('(P<academic_course_id>\d+)/(P<val>\d+)/', views.CourseListView.coursedetails, name='coursedetails'),
	path('coursedetails.html/',TemplateView.as_view(template_name='users/coursedetails.html'),name="coursevals"),
]
