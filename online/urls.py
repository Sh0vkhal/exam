from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('days', DayAPIViewSet, basename="day")
router.register('rooms', RoomAPIViewSet, basename="room")
router.register('courses', CourseAPIViewSet, basename="course")
router.register('courses-groups', CourseGroupAPIViewSet, basename="course_group")
router.register('like', LikeAPIViewSet, basename='like')
router.register('lessons', LessonAPIViewSet, basename='lesson')
router.register('attendance', AttendanceAPIViewSet, basename='attendance')
router.register('lesson-video', LessonVideoAPIViewSet, basename='video')
router.register('lesson-homework', LessonHomeworkAPIViewSet, basename='homework')
router.register('student-homework', StudentHomeworkAPIViewSet, basename='student-homewrok')
router.register('teacher', TeacherAPIViewSet, basename='teacher')
router.register('student', StudentAPIViewSet, basename='student')
urlpatterns = router.urls