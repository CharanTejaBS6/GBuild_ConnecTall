from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('subjects/', views.subjects, name='subjects'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('edit_subject/<int:subject_id>/',
         views.edit_subject, name='edit_subject'),
    path('delete_subject/<int:subject_id>/',
         views.delete_subject, name='delete_subject'),
    path('test-scores/', views.test_scores, name='test_scores'),
    path('add-test-score/', views.add_test_score, name='add_test_score'),
    path('edit-test-score/<int:test_score_id>/',
         views.edit_test_score, name='edit_test_score'),
    path('delete/<int:score_id>/', views.delete_test_score,
         name='delete_test_score'),
    path('attendance/', views.attendance_tracker, name='attendance_tracker'),
    path('update_attendance/<int:subject_id>/',
         views.update_attendance, name='update_attendance'),
    path('expense-tracker/', views.expense_tracker, name='expense_tracker'),
    #     path('notify/', views.send_notification_view, name='send_notification_view'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('add_event/', views.add_event, name='add_event'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignments/add/', views.add_assignment, name='add_assignment'),
    path('assignments/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('courses/', views.courses, name='courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    
]
