from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    short_form = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TestScore(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.marks}"


class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    present = models.PositiveIntegerField(default=0)
    absent = models.PositiveIntegerField(default=0)

    @property
    def total_classes(self):
        return self.present + self.absent

    @property
    def attendance_percentage(self):
        if self.total_classes > 0:
            return (self.present / self.total_classes) * 100
        else:
            return 0

    def __str__(self):
        return f"{self.subject.name} - Present: {self.present}, Absent: {self.absent}"


class Expense(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.item_name} - {self.date}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    given_date = models.DateField()
    submission_date = models.DateField()
    status_choices = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('late', 'Late'),
    )
    status = models.CharField(max_length=20, choices=status_choices)


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
