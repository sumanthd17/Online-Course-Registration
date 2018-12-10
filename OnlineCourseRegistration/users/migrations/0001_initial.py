from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'ADMIN'), ('student', 'STUDENT'), ('faculty', 'FACULTY'), ('guest', 'GUEST')], db_column='Role', max_length=45)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BufferSpecialPermissionsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req', models.TextField(max_length=200)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=45)),
                ('course_prof', models.CharField(max_length=45, null=True)),
                ('course_max_students', models.IntegerField(null=True)),
                ('course_delivery_mode', models.CharField(blank=True, max_length=45, null=True)),
                ('course_description', models.CharField(blank=True, max_length=80, null=True)),
                ('course_type', models.CharField(max_length=45)),
                ('courses_last_updated', models.DateTimeField(auto_now=True)),
                ('course_credits', models.SmallIntegerField()),
                ('course_rigour', models.CharField(db_column='course_Rigour', max_length=2)),
                ('course_hasprereqs', models.IntegerField(db_column='course_hasPrereqs')),
            ],
            options={
                'db_table': 'Course',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoursePreReqs',
            fields=[
                ('prereq_id', models.AutoField(auto_created=True, db_column='prereq_id', primary_key=True, serialize=False)),
                ('prereq_min_grade', models.CharField(db_column='preReq_min_grade', max_length=4)),
                ('prereq_descr', models.CharField(db_column='preReq_descr', max_length=45)),
                ('prereq_last_updated', models.DateTimeField(auto_now=True, db_column='preReq_last_updated')),
                ('prereq_courseid', models.ForeignKey(db_column='prereq_courseid', on_delete=django.db.models.deletion.DO_NOTHING, related_name='prereq_courseid', to='users.Course')),
                ('prereq_currentcourse', models.ForeignKey(db_column='prereq_currentcourse', on_delete=django.db.models.deletion.DO_NOTHING, related_name='prereq_currentcourse', to='users.Course')),
                ('prereq_last_accessby', models.ForeignKey(db_column='prereq_last_accessby', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Course_PreReqs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Courseregistrations',
            fields=[
                ('courseregistrations_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('courseregistrations_last_updated', models.DateTimeField(auto_now=True, db_column='courseRegistrations_last_updated')),
                ('courseregistrations_semester', models.CharField(db_column='courseRegistrations_semester', max_length=15)),
                ('courseregistrations_year', models.CharField(db_column='courseRegistrations_year', max_length=45)),
                ('courseregistrations_offeredto', models.CharField(db_column='courseRegistrations_offeredTo', max_length=45)),
                ('courseregistrations_classsize', models.CharField(db_column='courseRegistrations_classSize', max_length=45)),
                ('courseregistrations_startdate', models.DateField(db_column='courseRegistrations_StartDate')),
                ('courseregistrations_enddate', models.DateField(db_column='courseRegistrations_EndDate')),
                ('courseregistrations_updatedate', models.DateField(db_column='courseRegistrations_UpdateDate')),
                ('courseregistrations_finaldate', models.DateField(db_column='courseRegistrations_FinalDate')),
                ('courseregistrations_isactive', models.BooleanField(db_column='courseRegistrations_isActive', default=False)),
                ('courseregistrations_cid', models.ForeignKey(db_column='courseRegistrations_cid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
            ],
            options={
                'db_table': 'CourseRegistrations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.AutoField(auto_created=True, db_column='Faculty_id', primary_key=True, serialize=False)),
                ('faculty_name', models.CharField(db_column='Faculty_name', max_length=80)),
                ('faculty_email_id', models.CharField(db_column='Faculty_email_id', max_length=45)),
                ('faculty_designation', models.CharField(db_column='Faculty_designation', max_length=45)),
                ('faculty_last_updated', models.DateTimeField(auto_now=True, db_column='Faculty_last_updated')),
                ('faculty_userid', models.ForeignKey(db_column='Faculty_UserId', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Faculty',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FacultyCourseOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_course_offer_last_updated', models.DateTimeField(auto_now=True, db_column='Faculty_Course_offer_last_updated')),
                ('faculty_course_offer_last_access', models.CharField(db_column='Faculty_Course_offer_last_access', max_length=45)),
                ('courseid', models.ForeignKey(db_column='Courseid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
                ('facultyid', models.ForeignKey(db_column='Facultyid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Faculty')),
            ],
            options={
                'db_table': 'Faculty_Course_offer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FinalStudentRegistrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_studentregistrations_last_updated', models.DateTimeField(auto_now=True, db_column='final_studentregistrations_last_updated')),
                ('final_studentregistrations_cid', models.ForeignKey(db_column='final_studentRegistrations_cid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
            ],
            options={
                'db_table': 'FinalStudentRegistrations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, null=True)),
                ('course', models.CharField(max_length=20, null=True)),
                ('grade_point', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('grade_id', models.AutoField(db_column='grade_id', primary_key=True, serialize=False)),
                ('course_grade', models.CharField(max_length=3)),
                ('course_offered_year', models.CharField(max_length=45)),
                ('course_completed_year', models.CharField(blank=True, max_length=45, null=True)),
                ('course_sem', models.CharField(max_length=45)),
                ('grades_last_updated', models.DateTimeField(auto_now=True, max_length=45)),
                ('course_status', models.CharField(default='Not Started', max_length=30)),
                ('approval_comments', models.CharField(blank=True, db_column='approval_comments', max_length=200, null=True)),
                ('courseid', models.ForeignKey(db_column='courseid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
                ('grade_approvedby', models.ForeignKey(db_column='grade_approvedby', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Grades',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RegistrationPolicy',
            fields=[
                ('regPolicy_Id', models.AutoField(auto_created=True, db_column='regPolicy_Id', primary_key=True, serialize=False)),
                ('regPolicy_coursetype', models.CharField(db_column='regPolicy_coursetype', max_length=45)),
                ('regPolicy_year', models.CharField(db_column='regPolicy_year', max_length=45)),
                ('regPolicy_credits', models.IntegerField(db_column='regPolicy_credits')),
                ('regPolicy_last_updated', models.DateTimeField(auto_now=True, db_column='regPolicy_last_updated')),
                ('regPolicy_updateddby', models.ForeignKey(db_column='regPolicy_updatedby', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'registrationPolicy',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SpecialPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req', models.CharField(max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_roll_no', models.CharField(db_column='Student_roll_no', max_length=30, primary_key=True, serialize=False)),
                ('student_first_name', models.CharField(db_column='Student_First_Name', max_length=100)),
                ('student_middle_name', models.CharField(blank=True, db_column='Student_Middle_Name', max_length=100)),
                ('student_last_name', models.CharField(db_column='Student_Last_Name', max_length=100)),
                ('student_dob', models.DateField(blank=True, db_column='Student_dob', null=True)),
                ('student_gender', models.CharField(db_column='Student_Gender', max_length=6)),
                ('student_mobile', models.CharField(db_column='Student_mobile', max_length=15)),
                ('student_email', models.CharField(db_column='Student_email', max_length=45)),
                ('student_blood_group', models.CharField(db_column='Student_BloodGroup', max_length=4)),
                ('student_mother_tongue', models.CharField(db_column='Student_MotherTongue', max_length=45)),
                ('student_reg_year', models.CharField(db_column='Student_Registered_Year', max_length=10)),
                ('student_cur_year', models.CharField(db_column='Student_Current_Year', max_length=10)),
                ('student_curr_sem', models.CharField(db_column='Student_curr_sem', max_length=10)),
                ('student_degree', models.CharField(db_column='Student_degree', max_length=15)),
                ('student_degree_duration', models.CharField(db_column='Student_Degree_Duration', max_length=15)),
                ('student_academic_status', models.CharField(blank=True, db_column='Student_Academic_Status', max_length=20, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, max_length=45)),
                ('student_cgpa', models.FloatField(db_column='Student_cgpa', default=0.0)),
            ],
            options={
                'db_table': 'Student',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StudentEducPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_educ_last_updated', models.DateTimeField(auto_now=True, db_column='Student_Educ_last_updated', max_length=45)),
                ('student_educ_pref_last_accessed', models.CharField(db_column='Student_Educ_Pref_last_accessed', max_length=45)),
                ('student_educ_courseid', models.ForeignKey(db_column='Student_Educ_courseid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
                ('student_educ_studid', models.ForeignKey(db_column='Student_Educ_Studid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Student')),
            ],
            options={
                'db_table': 'Student_Educ_Pref',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Studentregistrations',
            fields=[
                ('studentregistrations_id', models.AutoField(auto_created=True, db_column='studentRegistrations_id', primary_key=True, serialize=False)),
                ('studentregistrations_preferences', models.CharField(blank=True, db_column='studentRegistrations_preferences', max_length=45, null=True)),
                ('studentregistrations_auditoption', models.CharField(blank=True, db_column='studentRegistrations_auditOption', max_length=10, null=True)),
                ('studentregistrations_approvedby', models.IntegerField(blank=True, db_column='studentRegistrations_approvedBy', null=True)),
                ('studentregistrations_status', models.CharField(db_column='studentRegistrations_status', max_length=10)),
                ('studentregistrations_comments', models.CharField(blank=True, db_column='studentRegistrations_comments', max_length=200, null=True)),
                ('studentregistrations_last_updated', models.DateTimeField(auto_now=True, db_column='Student_Spe_Req_last_updated')),
                ('studentregistrations_semester', models.CharField(blank=True, db_column='studentRegistrations_semester', default=' ', max_length=15, null=True)),
                ('studentregistrations_year', models.IntegerField(blank=True, db_column='studentRegistrations_year', default=2018)),
                ('studentregistrations_cid', models.ForeignKey(db_column='studentRegistrations_cid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
                ('studentregistrations_sid', models.ForeignKey(db_column='studentRegistrations_sid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Student')),
            ],
            options={
                'db_table': 'studentRegistrations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StudentSpeReq',
            fields=[
                ('student_spe_req_id', models.AutoField(auto_created=True, db_column='Student_Spe_Req_id', primary_key=True, serialize=False)),
                ('student_spe_req_descr', models.CharField(db_column='Student_Spe_Req_descr', max_length=45)),
                ('student_spe_req_status', models.CharField(db_column='Student_Spe_Req_status', max_length=45)),
                ('student_spe_req_last_updated', models.DateTimeField(auto_now=True, db_column='Student_Spe_Req_last_updated')),
                ('student_spe_req_last_access', models.CharField(blank=True, db_column='Student_Spe_Req_last_access', max_length=45, null=True)),
                ('student_spe_req_cid', models.ForeignKey(db_column='Student_Spe_Req_cid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Course')),
                ('student_spe_req_studid', models.ForeignKey(db_column='Student_Spe_Req_studid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Student')),
            ],
            options={
                'db_table': 'Student_Spe_Req',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='grades',
            name='studentid',
            field=models.ForeignKey(db_column='studentid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Student'),
        ),
        migrations.AddField(
            model_name='finalstudentregistrations',
            name='final_studentregistrations_sid',
            field=models.ForeignKey(db_column='final_studentRegistrations_sid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Student'),
        ),
        migrations.AddField(
            model_name='courseregistrations',
            name='courseregistrations_fid',
            field=models.ForeignKey(db_column='courseRegistrations_fid', on_delete=django.db.models.deletion.DO_NOTHING, to='users.Faculty'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('course_id', 'course_name')},
        ),
        migrations.AddField(
            model_name='bufferspecialpermissionstable',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='studentregistrations',
            unique_together={('studentregistrations_cid', 'studentregistrations_sid')},
        ),
        migrations.AlterUniqueTogether(
            name='registrationpolicy',
            unique_together={('regPolicy_coursetype', 'regPolicy_year', 'regPolicy_credits')},
        ),
        migrations.AlterUniqueTogether(
            name='grades',
            unique_together={('studentid', 'courseid')},
        ),
        migrations.AlterUniqueTogether(
            name='courseregistrations',
            unique_together={('courseregistrations_cid', 'courseregistrations_fid', 'courseregistrations_isactive')},
        ),
        migrations.AlterUniqueTogether(
            name='courseprereqs',
            unique_together={('prereq_currentcourse', 'prereq_courseid')},
        ),
    ]
