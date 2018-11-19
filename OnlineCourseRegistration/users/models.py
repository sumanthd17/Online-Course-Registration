# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser,Group,User,Permission



# Create your models here.
   
class CustomUser(AbstractUser):

	def __str__(self):
		return self.email

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=45)
    course_prof = models.CharField(max_length=45, null=True)
    course_max_students = models.IntegerField(null=True)
    course_delivery_mode = models.CharField(max_length=45, blank=True, null=True)
    course_description = models.CharField(max_length=80, blank=True, null=True)
    course_type = models.CharField(max_length=45)
    courses_last_updated = models.DateTimeField(auto_now=True)  # Field name made lowercase.(auto_now=True)
    course_credits = models.SmallIntegerField()
    course_rigour = models.CharField(db_column='course_Rigour', max_length=2)  # Field name made lowercase.
    course_hasprereqs = models.IntegerField(db_column='course_hasPrereqs')  # Field name made lowercase.
   
    class Meta:
        managed = True
        db_table = 'Course'

class SpecialPermissions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    req = models.CharField(max_length=20)

    def __str__(self):
        return self.req

class BufferSpecialPermissionsTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    req = models.TextField(max_length=200)
    status = models.CharField(max_length=20, default='pending')
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.req

class Grade(models.Model):
    student_id = models.CharField(max_length=20, null=True)
    course = models.CharField(max_length=20, null=True)
    grade_point = models.CharField(max_length=20, null=True)

    def __str__(self):
        return u'%s - %s - %s' % (self.student_id, self.course, self.grade_point)
  
class Faculty(models.Model):
    faculty_id = models.IntegerField(db_column='Faculty_id', primary_key=True)  # Field name made lowercase.
    faculty_name = models.CharField(db_column='Faculty_name', max_length=80)  # Field name made lowercase.
    faculty_email_id = models.CharField(db_column='Faculty_email_id', max_length=45)  # Field name made lowercase.
    faculty_designation = models.CharField(db_column='Faculty_designation', max_length=45)  # Field name made lowercase.
    faculty_last_updated = models.DateTimeField(db_column='Faculty_last_updated', auto_now=True)  # Field name made lowercase.
    faculty_userid = models.ForeignKey('CustomUser',models.DO_NOTHING,db_column='Facutly_UserId')

    class Meta:
        managed = True
        db_table = 'Faculty'


class FacultyCourseOffer(models.Model):
    facultyid = models.ForeignKey(Faculty, models.DO_NOTHING, db_column='Facultyid')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='Courseid')  # Field name made lowercase.
    faculty_course_offer_last_updated = models.DateTimeField(db_column='Faculty_Course_offer_last_updated',auto_now=True)  # Field name made lowercase.
    faculty_course_offer_last_access = models.CharField(db_column='Faculty_Course_offer_last_access', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Faculty_Course_offer'


class Grades(models.Model):
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='studentid')
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseid')
    course_grade = models.CharField(max_length=3)
    course_offered_year = models.CharField(max_length=45)
    course_sem = models.CharField(max_length=45)
    grades_last_updated = models.DateTimeField(max_length=45,auto_now=True)

    class Meta:
        managed = True
        db_table = 'Grades'



class Student(models.Model):
	student_roll_no = models.IntegerField(db_column='Student_roll_no', primary_key=True)
	student_first_name = models.CharField(db_column='Student_First_Name', max_length=100,null=False)
	student_middle_name = models.CharField(db_column='Student_Middle_Name', max_length=100,blank=True)
	student_last_name = models.CharField(db_column='Student_Last_Name', max_length=100,null=False)
	student_dob = models.DateField(db_column='Student_dob', blank=True, null=True)
	student_gender = models.CharField(db_column='Student_Gender', max_length=6,null=False)
	student_mobile = models.CharField(db_column='Student_mobile', max_length=15)
	student_email = models.CharField(db_column='Student_email', max_length=45)
	student_blood_group = models.CharField(db_column='Student_BloodGroup',max_length=4,null=False)
	student_mother_tongue = models.CharField(db_column='Student_MotherTongue',max_length=45,null=False)
	student_reg_year = models.CharField(db_column='Student_Registered_Year', max_length=10,null=False)
	student_cur_year = models.CharField(db_column='Student_Current_Year',max_length=10,null=False)
	student_curr_sem = models.CharField(db_column='Student_curr_sem', max_length=5,null=False)
	student_degree = models.CharField(db_column='Student_degree', max_length=15,null=False)
	student_degree_duration = models.CharField(db_column='Student_Degree_Duration',max_length=15,null=False)
	student_academic_status = models.CharField(db_column='Student_Academic_Status',max_length=20,blank=False,null=False)
	last_updated = models.DateTimeField(max_length=45,auto_now=True)
	student_Id = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='Student_Id')  # Field name made lowercase.
	
	class Meta:
		managed = True
		db_table = 'Student'

class StudentEducPref(models.Model):
    student_educ_studid = models.ForeignKey(Student, models.DO_NOTHING, db_column='Student_Educ_Studid')  # Field name made lowercase.
    student_educ_courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='Student_Educ_courseid')  # Field name made lowercase.
    student_educ_last_updated = models.DateTimeField(db_column='Student_Educ_last_updated', max_length=45,auto_now=True)  # Field name made lowercase.
    student_educ_pref_last_accessed = models.CharField(db_column='Student_Educ_Pref_last_accessed', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Student_Educ_Pref'


class StudentSpeReq(models.Model):
    student_spe_req_id = models.IntegerField(db_column='Student_Spe_Req_id', primary_key=True)  # Field name made lowercase.
    student_spe_req_studid = models.ForeignKey(Student, models.DO_NOTHING, db_column='Student_Spe_Req_studid')  # Field name made lowercase.
    student_spe_req_cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='Student_Spe_Req_cid')  # Field name made lowercase.
    student_spe_req_descr = models.CharField(db_column='Student_Spe_Req_descr', max_length=45)  # Field name made lowercase.
    student_spe_req_status = models.CharField(db_column='Student_Spe_Req_status', max_length=45)  # Field name made lowercase.
    student_spe_req_last_updated = models.DateTimeField(db_column='Student_Spe_Req_last_updated', auto_now=True)  # Field name made lowercase.
    student_spe_req_last_access = models.CharField(db_column='Student_Spe_Req_last_access', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Student_Spe_Req'


class Courseregistrations(models.Model):
    courseregistrations_id = models.AutoField(primary_key=True)
    courseregistrations_cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseRegistrations_cid')  # Field name made lowercase.
    courseregistrations_fid = models.ForeignKey(Faculty, models.DO_NOTHING, db_column='courseRegistrations_fid')  # Field name made lowercase.
    courseregistrations_last_updated = models.DateTimeField(db_column='courseRegistrations_last_updated',auto_now=True)  # Field name made lowercase.
    courseregistrations_semester = models.CharField(db_column='courseRegistrations_semester', max_length=15)  # Field name made lowercase.
    courseregistrations_year = models.CharField(db_column='courseRegistrations_year', max_length=45)  # Field name made lowercase.
    courseregistrations_offeredto = models.CharField(db_column='courseRegistrations_offeredTo', max_length=45)  # Field name made lowercase.
    courseregistrations_classsize = models.CharField(db_column='courseRegistrations_classSize', max_length=45)  # Field name made lowercase.
    courseregistrations_startdate = models.DateTimeField(db_column='courseRegistrations_StartDate')  # Field name made lowercase.
    courseregistrations_enddate = models.DateTimeField(db_column='courseRegistrations_EndDate')  # Field name made lowercase.
    courseregistrations_updatedate = models.DateTimeField(db_column='courseRegistrations_UpdateDate')  # Field name made lowercase.
    courseregistrations_finaldate = models.DateTimeField(db_column='courseRegistrations_FinalDate')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CourseRegistrations'
        unique_together = (('courseregistrations_cid', 'courseregistrations_fid'),)




class CoursePreReq(models.Model):
    present_course = models.ForeignKey(Course, models.DO_NOTHING)
    course_pre_req_id = models.IntegerField(db_column='Course_Pre_Req_id')  # Field name made lowercase.
    course_pre_req_min_grade = models.CharField(db_column='Course_Pre_Req_min_grade', max_length=4)  # Field name made lowercase.
    course_pre_req_descr = models.CharField(db_column='Course_Pre_Req_descr', max_length=45)  # Field name made lowercase.
    course_pre_req_last_updated = models.DateTimeField(db_column='Course_Pre_Req_last_updated', auto_now=True)  # Field name made lowercase.
    course_pre_req_last_access_by = models.CharField(db_column='Course_Pre_Req_last_access_by', max_length=45)
    
    class Meta:
    	managed = True
    	db_table = 'Course_Pre_Req'


class Studentregistrations(models.Model):
    studentregistrations_id = models.AutoField(auto_created=True,db_column='studentRegistrations_id', primary_key=True)  # Field name made lowercase.
    studentregistrations_cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='studentRegistrations_cid')  # Field name made lowercase.
    studentregistrations_sid = models.ForeignKey(Student, models.DO_NOTHING, db_column='studentRegistrations_sid')  # Field name made lowercase.
    studentregistrations_preferences = models.CharField(db_column='studentRegistrations_preferences', max_length=45, blank=True, null=True)  # Field name made lowercase.
    studentregistrations_auditoption = models.IntegerField(db_column='studentRegistrations_auditOption', blank=True, null=True)  # Field name made lowercase.
    studentregistrations_approvedby = models.IntegerField(db_column='studentRegistrations_approvedBy', blank=True, null=True)  # Field name made lowercase.
    studentregistrations_status = models.CharField(db_column='studentRegistrations_status', max_length=10)  # Field name made lowercase.
    studentregistrations_comments = models.CharField(db_column='studentRegistrations_comments', max_length=200, blank=True, null=True)  # Field name made lowercase.
    studentregistrations_last_updated = models.DateTimeField(db_column='Student_Spe_Req_last_updated', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'studentRegistrations'
        unique_together = (('studentregistrations_cid', 'studentregistrations_sid'),)
