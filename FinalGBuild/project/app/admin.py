from django.contrib import admin
from .models import Subject, TestScore, Attendance, Event, Assignment, Course,Expense
# Register your models here.
admin.site.register(Subject)
admin.site.register(TestScore)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(Assignment)
admin.site.register(Course)
admin.site.register(Expense)
