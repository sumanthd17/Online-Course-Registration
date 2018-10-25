from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

	def __str__(self):
		return self.email

class Course(models.Model):
	name = models.CharField(max_length=20)
	prof = models.CharField(max_length=20)
	max_students = models.IntegerField()

	def __str__(self):
		return u'%s %s' % (self.name, self.prof)

class Detail(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	min_GPA = models.IntegerField()
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.description


class AuditCourse(models.Model):
	roll = models.CharField(max_length=20)
	name = models.CharField(max_length=20)