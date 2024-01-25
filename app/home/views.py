from django.shortcuts import render
from . import models


def index(request):
    return render(request, "home/index.html", {})


def golf_courses(request):
    course_list = models.GolfCourse.objects.all()
    return render(request, "home/golf-courses.html", {"course_list": course_list})


def golf_course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(request, "home/golf-course-detail.html", {"obj": course_data})
