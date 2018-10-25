from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('', views.index, name='index'),
	path('<int:course_id>/', views.details, name='details'),
	path('add_course/', views.add_course, name='add_course'),
	path('audit_course/', views.audit_course, name='audit_course'),
	path('<int:course_id>/add_course_details/', views.add_course_details, name='add_course_details'),
]