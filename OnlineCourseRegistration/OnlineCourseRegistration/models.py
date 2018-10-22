# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcademicBatch(models.Model):
    academic_batch_id = models.IntegerField(db_column='Academic_Batch_Id', primary_key=True,unique=True)  # Field name made lowercase.
    academic_batch_number = models.IntegerField(db_column='Academic_Batch_Number')  # Field name made lowercase.
    academic_batch_degree = models.ForeignKey('AcademicDegree', models.DO_NOTHING, related_name='Academic_Batch_Academic_Degree_Id')  # Field name made lowercase.
    academic_batch_start_year = models.DateField(db_column='Academic_Batch_Start_Year')  # Field name made lowercase.
    academic_batch_end_year = models.DateField(db_column='Academic_Batch_End_Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Academic_Batch'
        unique_together = (('academic_batch_degree', 'academic_batch_start_year'),)


class AcademicCourse(models.Model):
    academic_course_id = models.IntegerField(db_column='Academic_Course_Id', primary_key=True,unique=True)  # Field name made lowercase.
    academic_course_name = models.CharField(db_column='Academic_Course_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    academic_course_rigour = models.CharField(db_column='Academic_Course_Rigour', max_length=2)  # Field name made lowercase.
    academic_course_level = models.IntegerField(db_column='Academic_Course_Level')  # Field name made lowercase.
    academic_course_pre_req = models.CharField(db_column='Academic_Course_Pre-Req', max_length=1)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    academic_cours_delivery_mode = models.IntegerField(db_column='Academic_Cours_Delivery_Mode')  # Field name made lowercase.
    academic_course_description = models.CharField(db_column='Academic_Course_Description', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Academic_Course'


class AcademicDegree(models.Model):
    academic_degree_id = models.IntegerField(db_column='Academic_Degree_Id', primary_key=True,unique=True)  # Field name made lowercase.
    academic_degree_name = models.CharField(db_column='Academic_Degree_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    academic_degree_start_year = models.DateField(db_column='Academic_Degree_Start_Year', blank=True, null=True)  # Field name made lowercase.
    academic_degree_duration = models.DateField(db_column='Academic_Degree_Duration', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Academic_Degree'


class AcademicProgBatchSemCourse(models.Model):
    academic_prog_batch_sem_course_id = models.IntegerField(db_column='Academic_Prog_Batch_Sem_Course_Id', primary_key=True,unique=True)  # Field name made lowercase.
    academic_prog_batch_sem_course_batch = models.ForeignKey(AcademicBatch, models.DO_NOTHING, related_name='Academic_Prog_Batch_Sem_Course_Academic_Batch_Id')  # Field name made lowercase.
    academic_prog_batch_sem_course_sem_num = models.IntegerField(db_column='Academic_Prog_Batch_Sem_Course_Sem_Num')  # Field name made lowercase.
    academic_prog_batch_sem_course_course = models.ForeignKey(AcademicCourse, models.DO_NOTHING, related_name='Academic_Prog_Batch_Sem_Course_Academic_Course_Id')  # Field name made lowercase.
    academic_prog_batch_sem_course_credits = models.IntegerField(db_column='Academic_Prog_Batch_Sem_Course_Credits', blank=True, null=True)  # Field name made lowercase.
    academic_prog_batch_sem_course_eval_code = models.CharField(db_column='Academic_Prog_Batch_Sem_Course_Eval_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    academic_prog_batch_sem_course_status = models.CharField(db_column='Academic_Prog_Batch_Sem_Course_Status', max_length=45, blank=True, null=True)  # Field name made lowercase.
    academic_prog_batch_sem_coursecol = models.CharField(db_column='Academic_Prog_Batch_Sem_Coursecol', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Academic_Prog_Batch_Sem_Course'


class CourseAcadPerfEval(models.Model):
    course_acad_perf_eval_id = models.IntegerField(db_column='Course_Acad_Perf_Eval_Id', primary_key=True,unique=True)  # Field name made lowercase.
    course_acad_perf_eval_std_sem_cou = models.ForeignKey(AcademicProgBatchSemCourse, models.DO_NOTHING, related_name='Course_Acad_Perf_Eval_Std_Academic_Sem_Cou_ID')  # Field name made lowercase.
    course_academic_performance_test_no = models.IntegerField(db_column='Course_Academic_Performance_Test_no')  # Field name made lowercase.
    course_academic_performance_type_of_exam = models.CharField(db_column='Course_Academic_Performance_Type_Of Exam', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    course_academic_performance_weightage = models.IntegerField(db_column='Course_Academic_Performance_Weightage')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Course_Acad_Perf_Eval'


class Department(models.Model):
    department_id = models.IntegerField(db_column='Department_Id', primary_key=True,unique=True)  # Field name made lowercase.
    department_name = models.CharField(db_column='Department_Name', max_length=45)  # Field name made lowercase.
    department_head_position = models.CharField(db_column='Department_Head_Position', max_length=45)  # Field name made lowercase.
    department_head_emp_id = models.IntegerField(db_column='Department_Head_Emp_Id')  # Field name made lowercase.
    department_isfaculty = models.CharField(db_column='Department_IsFaculty', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Department'


class Employee(models.Model):
    employee_id = models.IntegerField(db_column='Employee_Id', primary_key=True,unique=True)  # Field name made lowercase.
    employee_reg_no = models.CharField(db_column='Employee_Reg_No', unique=True, max_length=45)  # Field name made lowercase.
    employee_first_name = models.CharField(db_column='Employee_First_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    employee_second_name = models.CharField(db_column='Employee_Second_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    employee_last_name = models.CharField(db_column='Employee_Last_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    employee_name_for_email = models.CharField(db_column='Employee_Name_for_Email', max_length=60)  # Field name made lowercase.
    employee_dept = models.ForeignKey(Department, models.DO_NOTHING, related_name='Employee_Dept_Department_Id')  # Field name made lowercase.
    employee_doj = models.DateField(db_column='Employee_DOJ')  # Field name made lowercase.
    employee_manager = models.ForeignKey('self', models.DO_NOTHING, db_column='Employee_Manager', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employee'


class FacultyCourse(models.Model):
    faculty_course_id = models.IntegerField(db_column='Faculty_Course_Id', primary_key=True,unique=True)  # Field name made lowercase.
    faculty_course_employee = models.ForeignKey(Employee, models.DO_NOTHING, related_name='Faculty_Course_Employee_Employee_Id')  # Field name made lowercase.
    faculty_course_courses = models.ForeignKey(AcademicProgBatchSemCourse, models.DO_NOTHING, related_name='Faculty_Course_Coures_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Faculty_Course'


class StdAcadPerf(models.Model):
    std_acad_perf_id = models.IntegerField(db_column='Std_Acad_Perf_Id', primary_key=True,unique=True)  # Field name made lowercase.
    std_acad_perf_student = models.ForeignKey('Student', models.DO_NOTHING, related_name='Std_Acad_Perf_Student_Student_Id')  # Field name made lowercase.
    std_acad_perf_course_acad_perf_eval = models.ForeignKey(CourseAcadPerfEval, models.DO_NOTHING, db_column='Std_Acad_Perf_Course_Acad_Perf_Eval')  # Field name made lowercase.
    std_acad_perf = models.IntegerField(db_column='Std_Acad_Perf')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Std_Acad_Perf'


class Student(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True,unique=True)  # Field name made lowercase.
    student_id = models.IntegerField(db_column='Student_Id', unique=True)  # Field name made lowercase.
    student_first_name = models.CharField(db_column='Student_First_Name', max_length=45)  # Field name made lowercase.
    student_middle_name = models.CharField(db_column='Student_Middle_Name', max_length=90, blank=True, null=True)  # Field name made lowercase.
    student_last_name = models.CharField(db_column='Student_Last_name', max_length=45)  # Field name made lowercase.
    student_dob = models.DateField(db_column='Student_DOB')  # Field name made lowercase.
    student_gender = models.CharField(db_column='Student_Gender', max_length=1)  # Field name made lowercase.
    student_email = models.CharField(db_column='Student_Email', max_length=45, blank=True, null=True)  # Field name made lowercase.
    student_mobile = models.CharField(db_column='Student_Mobile', max_length=10, blank=True, null=True)  # Field name made lowercase.
    student_blood_group = models.CharField(db_column='Student_Blood_Group', max_length=4)  # Field name made lowercase.
    student_mother_tongue = models.CharField(db_column='Student_Mother_Tongue', max_length=45, blank=True, null=True)  # Field name made lowercase.
    student_registered_year = models.DateField(db_column='Student_Registered_Year', blank=True, null=True)  # Field name made lowercase.
    student_registered_degree = models.ForeignKey(AcademicBatch, models.DO_NOTHING, related_name='Student_Registered_Degree_Academic_Batch_Id')  # Field name made lowercase.
    student_registered_degree_duration = models.DateField(db_column='Student_Registered_Degree_Duration')  # Field name made lowercase.
    student_cur_yearofstudy = models.DateField(db_column='Student_Cur_YearofStudy')  # Field name made lowercase.
    student_cur_sem = models.IntegerField(db_column='Student_Cur_Sem')  # Field name made lowercase.
    student_academic_status = models.CharField(db_column='Student_Academic_Status', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student'


class StudentEducHist(models.Model):
    student_educ_hist_id = models.IntegerField(db_column='Student_Educ_Hist_id', primary_key=True,unique=True)  # Field name made lowercase.
    student_educ_stud = models.ForeignKey(Student, models.DO_NOTHING, db_column='Student_Educ_Stud_Student_Id')  # Field name made lowercase.
    student_educ_yr_pass = models.CharField(db_column='Student_Educ_Yr_pass', max_length=6)  # Field name made lowercase.
    student_educ_hist_degree = models.CharField(db_column='Student_Educ_Hist_Degree', max_length=45)  # Field name made lowercase.
    student_educ_hist_regno = models.CharField(db_column='Student_Educ_Hist_RegNo', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student_Educ_Hist'


class StudentParent(models.Model):
    student_parent_id = models.IntegerField(db_column='Student_Parent_Id', primary_key=True,unique=True)  # Field name made lowercase.
    student_parent_student = models.ForeignKey(Student, models.DO_NOTHING, related_name='Student_Parent_Student_Student_Id')  # Field name made lowercase.
    student_parent_student_relation = models.CharField(db_column='Student_Parent_Student_Relation', max_length=1)  # Field name made lowercase.
    student_parent_first_name = models.CharField(db_column='Student_Parent_"First_Name', max_length=45)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    student_parent_middle_name = models.CharField(db_column='Student_Parent_Middle_Name', max_length=90, blank=True, null=True)  # Field name made lowercase.
    student_parent_last_name = models.CharField(db_column='Student_Parent_Last_Name', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student_Parent'


class StudentSemCourseReg(models.Model):
    student_sem_course_reg_id = models.IntegerField(db_column='Student_Sem_Course_Reg_Id', primary_key=True,unique=True)  # Field name made lowercase.
    student_sem_course_reg_student = models.ForeignKey(Student, models.DO_NOTHING, related_name='Student_Sem_Course_Reg_Student_Id')  # Field name made lowercase.
    student_sem_course_reg_batch_sem_course = models.ForeignKey(AcademicProgBatchSemCourse, models.DO_NOTHING, db_column='Student_Sem_Course_Reg_Batch_Sem_Course_AcademicProgBatchSemCourse_Id')  # Field name made lowercase.
    student_sem_course_reg_reg_status = models.CharField(db_column='Student_Sem_Course_Reg_Reg_Status', max_length=1)  # Field name made lowercase.
    student_sem_course_reg_req_date = models.DateField(db_column='Student_Sem_Course_Reg_Req_Date')  # Field name made lowercase.
    student_sem_course_reg_approve_date = models.DateField(db_column='Student_Sem_Course_Reg_Approve_Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Student_Sem_Course_Reg'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class UsersCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_customuser'


class UsersCustomuserGroups(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)
