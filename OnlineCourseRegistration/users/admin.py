from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import Course,Student,Courseregistrations,CoursePreReq,Faculty,Grades,StudentEducPref,User,StudentSpeReq,Studentregistrations, FinalStudentRegistrations



# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username',]
	
CustomUser = get_user_model()
	
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Grades)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(CoursePreReq)
admin.site.register(Studentregistrations)
admin.site.register(FinalStudentRegistrations)