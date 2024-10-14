from django.contrib import admin

from .models import *

admin.site.register(Days)
admin.site.register(Room)
admin.site.register(Course)
admin.site.register(CourseGroup)
admin.site.register(Lesson)
admin.site.register(LessonVideo)
admin.site.register(LessonHomework)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(StudentHomework)
admin.site.register(Attendance)
admin.site.register(Like)
