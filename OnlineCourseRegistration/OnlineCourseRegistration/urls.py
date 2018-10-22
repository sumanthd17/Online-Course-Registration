"""OnlineCourseRegistration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from OnlineCourseRegistration.views import CourseListView




urlpatterns = [
    url(r'^admin/', admin.site.urls),   
    url(r'^$',TemplateView.as_view(template_name='home.html'), name='home'), 
    url(r'index.html/$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'Students.html/$', TemplateView.as_view(template_name='Students.html'),name='Students'),
    url(r'course.html/$', TemplateView.as_view(template_name='course.html'),name='Subjects'),    
    url(r'courselist.html/', CourseListView.as_view(),name='MyCourseList'), 
     url(r'courselist.html/the_url', CourseListView.as_view(),name='details'),     
    url('users/', include('users.urls')),
	url('users/', include('django.contrib.auth.urls')), 
]
