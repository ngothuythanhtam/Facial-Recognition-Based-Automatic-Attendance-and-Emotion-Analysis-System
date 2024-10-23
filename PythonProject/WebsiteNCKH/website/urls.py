from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('gosystem/', views.gosystem, name='gosystem'),
    path('manageaccsystem/', views.manage_acc_system, name='manageaccsystem'),
    path('search_profile/', views.search_profile, name='search_profile'),
    # path('clear-course-session/', views.clear_course_session, name='clear_course_session'),
    path('attendance_currentcourse/', views.attendance_currentcourse, name='attendance_currentcourse'),
    path('search_result_attendance/', views.search_result_attendance, name='search_result_attendance'),
    path('result_search_attendance/', views.result_search_attendance, name='result_search_attendance'),
    path('ls_attflw_course/', views.ls_attflw_course, name='ls_attflw_course'),
    path('emotion/', views.emotion, name='emotion'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)