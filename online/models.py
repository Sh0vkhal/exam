from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import FileExtensionValidator


# Create your models here.


class Days(models.Model):
    """Dars bo'ladigan kunlar"""
    week_day = models.CharField(max_length=15)

    def __str__(self):
        return self.week_day


class Room(models.Model):
    """Dars bo'ladigan xonalar"""
    name = models.CharField(max_length=100)
    limit = models.IntegerField(default=16, help_text="O'quvchi sig'imi")

    def __str__(self):
        return self.name


class Course(models.Model):
    """Mavjud kurslar"""
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


STATUS = [
    ('not_started', "Boshlanmagan"),
    ('continue', "Davom etyapti"),
    ('ended', "Tugagan"),
    ('stopped', "To'xtailingan")
]


class CourseGroup(models.Model):
    """Kurs uchun ochilgan guruhlar"""
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=5, help_text="Guruh raqami. M: FN21")
    start_date = models.DateField()
    end_date = models.DateField()
    time_lesson = models.TimeField()
    days = models.ManyToManyField(Days)
    status = models.CharField(max_length=15, choices=STATUS)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)

    def __str__(self):
        return self.number


class Like(models.Model):
    """ Darslarni baholash (Yoqdi yoki yoqmadi)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | {self.liked}"


class Lesson(models.Model):
    """Guruhlar darslari"""
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    start_lesson = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=255, help_text="Dars mavzusi")
    liked = models.ForeignKey(Like, on_delete=models.CASCADE)

    def __str__(self):
        return self.theme


class Attendance(models.Model):
    """Davomat"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    came_to_class = models.DateTimeField(auto_now_add=True, help_text="Darsga kelgan vaqti")

    def __str__(self):
        return f"{self.student.user.username} | {self.came_to_class}"


class LessonVideo(models.Model):
    """Dars videosi"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE),
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to="media/videos/", validators=[FileExtensionValidator(['mp4', 'avi'])])

    def __str__(self):
        return self.name


class LessonHomework(models.Model):
    """Dars uchun uy ishi"""
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    given_time = models.DateTimeField(auto_now_add=True)
    duration = models.DateTimeField()
    text = models.TextField()
    file = models.FileField(upload_to="lesson/homework/", null=True, blank=True)

    def __str__(self):
        return f"Homework for lesson: {self.lesson}"


# ------------------------------------

class StudentHomework(models.Model):
    '''Talaba topshiradigan uy ishi'''
    lesson_homework = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    file = models.FileField(upload_to="student/homework/", null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} {self.lesson_homework.theme}"


# ------------------------------------

class Teacher(models.Model):
    """O'qituvchilar"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(CourseGroup)
    experience = models.IntegerField(default=1)
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Student(models.Model):
    """Talabalar"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(CourseGroup)
    is_study = models.BooleanField(default=False)