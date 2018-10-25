from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from .models import Course, Grade, AuditCourse

# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username',]
	
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
<<<<<<< HEAD
admin.site.register(Grade)
=======
admin.site.register(AuditCourse)
>>>>>>> 649b8068a6a841a7d569ed94e35e41f9478d173d
