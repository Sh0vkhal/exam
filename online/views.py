from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

from .models import *
from .serializers import *
from course.settings import EMAIL_HOST_USER


class DayAPIViewSet(ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class RoomAPIViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class CourseAPIViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class CourseGroupAPIViewSet(ModelViewSet):
    serializer_class = CourseGroupSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status")
        if status:
            return CourseGroup.objects.filter(status=status)
        return CourseGroup.objects.all()

    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class LikeAPIViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class LessonAPIViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['theme']


class AttendanceAPIViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class =AttendanceSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class LessonVideoAPIViewSet(ModelViewSet):
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class LessonHomeworkAPIViewSet(ModelViewSet):
    queryset =LessonHomework.objects.all()
    serializer_class = LessonHomeworkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class StudentHomeworkAPIViewSet(ModelViewSet):
    queryset = StudentHomework.objects.all()
    serializer_class = StudentHomeworkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class TeacherAPIViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class =TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class StudentAPIViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class MessageAPIView(APIView):
    def post(self, request):
        serializers = MessageSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        send_mail(
            subject=serializers.validated_data.get("title"),
            message=serializers.validated_data.get("message"),
            from_email= EMAIL_HOST_USER,
            recipient_list=[user.email for user in User.objects.all() if user.email],
            fail_silently=False
        )
        return Response("Habar yuborildi")
