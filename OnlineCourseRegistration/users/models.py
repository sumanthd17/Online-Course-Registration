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
		return u'%s - %s - %s' % (self.name, self.prof, self.max_students)

class Student(models.Model):
	name = models.CharField(max_length=30)
	roll = models.CharField(max_length=12)
	year = models.CharField(max_length=4)
	email = models.CharField(max_length=40)
	cgpa = models.FloatField(max_length=4,null=True)

	def __str__(self):
		return u'%s - %s - %s - %s - %s' % (self.name, self.roll, self.year, self.email, self.cgpa)

class Detail(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	min_GPA = models.IntegerField()
	description = models.CharField(max_length=200)

	def __str__(self):
		return u'%s %s %s' % (self.course, self.min_GPA, self.description)

class Grade(models.Model):
	student_id = models.CharField(max_length=20, null=True)
	course = models.CharField(max_length=20, null=True)
	grade_point = models.CharField(max_length=20, null=True)

	def __str__(self):
		return u'%s - %s - %s' % (self.student_id, self.course, self.grade_point)

class Register(models.Model):
	student_id = models.CharField(max_length=20, null=True)
	course = models.CharField(max_length=20, null=True)

	def __str__(self):
		return u'%s - %s' % (self.student_id, self.course) 

class AuditCourse(models.Model):
	roll = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
		
class AcademicCourse(models.Model):
    academic_course_id = models.IntegerField(db_column='Academic_Course_Id', primary_key=True,unique=True)  # Field name made lowercase.
    academic_course_name = models.CharField(db_column='Academic_Course_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    academic_course_rigour = models.CharField(db_column='Academic_Course_Rigour', max_length=2)  # Field name made lowercase.
    academic_course_level = models.IntegerField(db_column='Academic_Course_Level')  # Field name made lowercase.
    academic_course_pre_req = models.CharField(db_column='Academic_Course_Pre-Req', max_length=1)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    academic_cours_delivery_mode = models.IntegerField(db_column='Academic_Course_Delivery_Mode')  # Field name made lowercase.
    academic_course_description = models.CharField(db_column='Academic_Course_Description', max_length=250, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
    	return self.description

