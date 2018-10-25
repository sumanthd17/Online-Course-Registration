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

class Student(models.Model):
	name = models.CharField(max_length=30)
	roll = models.CharField(max_length=12)
	year = models.CharField(max_length=4)
	email = models.CharField(max_length=20)

	def __str__(self):
		return self.roll

class Detail(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	min_GPA = models.IntegerField()
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.description

class Grade(models.Model):
	student_id = models.CharField(max_length=20, null=True)
	course = models.CharField(max_length=20, null=True)
	grade_point = models.CharField(max_length=20, null=True)

	def __str__(self):
		return u'%s %s %s' % (self.student_id, self.course, self.grade_point)