from django.shortcuts import render
from . import models


def index(request):
    return render(request, "home/index.html", {})


def golf_courses(request):
    course_list = models.GolfCourse.objects.all()
    return render(request, "home/golf-courses.html", {"course_list": course_list})

