from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Subject
from .forms import SubjectForm
from .models import TestScore
from .forms import AddTestScoreForm, EditTestScoreForm
from django.contrib import messages
from .models import Attendance
from django.db.models import Sum, F
from .models import Expense, Event
from .forms import ExpenseForm, EventForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment
from .forms import AssignmentForm
from .models import Course
from .forms import CourseForm
from datetime import timedelta, datetime
from django.utils import timezone

# def send_notification_view(request):
#     # Example usage
#     subject = 'New Notification'
#     message = 'Hello from Django!'
#     recipient_list = ['srinivasareddybv6@email.com', 'mrhandsomecutehot@email.com']
#     send_mail(subject, message, 'charantej6ms@gmail.com', recipient_list)
#     return HttpResponse("Done")


def calendar_view(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'calendar.html', context)


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar_view')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def expense_tracker(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_tracker')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all()
    return render(request, 'expense_tracker.html', {'form': form, 'expenses': expenses})


def update_attendance(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    action = request.POST.get('action')

    if action == 'present':
        Attendance.objects.filter(subject=subject).update(
            present=F('present') + 1)
    elif action == 'absent':
        Attendance.objects.filter(subject=subject).update(
            absent=F('absent') + 1)

    return redirect('attendance_tracker')


def attendance_tracker(request):
    subjects = Subject.objects.all()
    attendance_data = []

    for subject in subjects:
        total_present = Attendance.objects.filter(
            subject=subject).aggregate(Sum('present'))['present__sum'] or 0
        total_absent = Attendance.objects.filter(
            subject=subject).aggregate(Sum('absent'))['absent__sum'] or 0
        total_classes = total_present + total_absent

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = (total_present / total_classes) * 100

        attendance_data.append({
            'subject': subject,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_classes': total_classes,
            'attendance_percentage': attendance_percentage,
        })

    return render(request, 'attendance_tracker.html', {'attendance_data': attendance_data})


def test_scores(request):
    test_scores = TestScore.objects.all()
    return render(request, 'test_scores.html', {'test_scores': test_scores})


def add_test_score(request):
    if request.method == 'POST':
        form = AddTestScoreForm(request.POST)
        if form.is_valid():
            test_score = form.save()
            return redirect('test_scores')
    else:
        form = AddTestScoreForm()
    return render(request, 'add_test_score.html', {'form': form})


def edit_test_score(request, test_score_id):
    test_score = TestScore.objects.get(pk=test_score_id)
    if request.method == 'POST':
        form = EditTestScoreForm(request.POST, instance=test_score)
        if form.is_valid():
            form.save()
            return redirect('test_scores')
    else:
        form = EditTestScoreForm(instance=test_score)
    return render(request, 'edit_test_score.html', {'form': form})


def delete_test_score(request, score_id):
    if request.method == 'POST':
        score = TestScore.objects.get(pk=score_id)
        score.delete()
        messages.success(request, 'Test score deleted successfully.')
        return redirect('test_scores')
    else:
        return redirect('test_scores')


def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})


# def add_subject(request):
#     if request.method == 'POST':
#         form = SubjectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('subjects')
#     else:
#         form = SubjectForm()
#     return render(request, 'add_subject.html', {'form': form})

# def mark_attendance(request, attendance_id, status):
#     attendance = Attendance.objects.get(pk=attendance_id)
#     if status == 'present':
#         attendance.present += 1
#     elif status == 'absent':
#         attendance.absent += 1
#     attendance.save()
#     return redirect('attendance_tracker')

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            # Automatically add a new subject to Attendance list
            Attendance.objects.create(subject=subject)
            return redirect('subjects')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})


def edit_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'edit_subject.html', {'form': form})


def delete_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    subject.delete()
    return redirect('subjects')


def index(request):
    return render(request, 'welcome.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def home(request):
    today = datetime.now().date()
    three_days_later = today + timedelta(days=3)

    upcoming_courses = Course.objects.filter(end_date__lte=three_days_later)
    upcoming_assignments = Assignment.objects.filter(
        submission_date__lte=three_days_later)

    upcoming_deadlines = []
    for course in upcoming_courses:
        upcoming_deadlines.append(
            f"Course Deadline: {course.name} - {course.end_date}")
    for assignment in upcoming_assignments:
        upcoming_deadlines.append(f"Assignment Deadline: {
                                  assignment.name} - {assignment.submission_date}")

    return render(request, 'home.html', {'upcoming_deadlines': upcoming_deadlines})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments.html', {'assignments': assignments})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return render(request, 'home.html')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})


def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form})


def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses')
    return render(request, 'delete_course.html', {'course': course})


def assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments.html', {'assignments': assignments})


def add_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignments')
    else:
        form = AssignmentForm()
    return render(request, 'add_assignment.html', {'form': form})


def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignments')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'edit_assignment.html', {'form': form})


def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')
    return render(request, 'delete_assignment.html', {'assignment': assignment})
