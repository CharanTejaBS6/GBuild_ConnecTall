

from django import forms
from .models import Subject
from .models import TestScore, Expense , Event , Assignment , Course


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['item_name', 'item_description', 'item_cost', 'date']


class AddTestScoreForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    marks = forms.FloatField()

    class Meta:
        model = TestScore
        fields = ['subject', 'marks']


class EditTestScoreForm(forms.ModelForm):
    marks = forms.FloatField()

    class Meta:
        model = TestScore
        fields = ['marks']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'short_form']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date']  
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'given_date', 'submission_date', 'status']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date']