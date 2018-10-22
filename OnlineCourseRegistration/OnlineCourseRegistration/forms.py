from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from users.models import CustomUser
from OnlineCourseRegistration.models import AcademicCourse

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'email')
		
class GetCourseList(ModelForm):	
	course_num = forms.IntegerField()
	course_name = forms.CharField()

	def __init__(self):
		if check_something():
			self.fields['is_selected'].initial  = False
	class Meta:
		model = AcademicCourse
		fields = ('academic_course_id','academic_course_name')	
