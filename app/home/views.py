from django.shortcuts import render, get_object_or_404, redirect
from . import models
from . import forms


def index(request):
    return render(request, "home/index.html", {})


def golf_courses(request):
    course_list = models.GolfCourse.objects.all()
    return render(request, "home/golf-courses.html", {"course_list": course_list})


def golf_course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(request, "home/golf-course-detail.html", {"obj": course_data})


def create_golf_course(request):
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST)
        if form.is_valid():
            course_data = form.save()
            hole_count = int(course_data.hole_count)
            for hole in range(hole_count):
                new_hole = models.Hole(
                    name=f"Hole: {hole + 1}",
                    order=hole,
                    course=course_data
                )
                new_hole.save()
            
            return redirect("home:golf-courses")
    else:
        form = forms.GolfCourseForm()
    return render(request, "home/form.html", {"form": form})


def hole_detail(request, pk):
    hole_data = get_object_or_404(models.Hole, pk=pk)
    course_data = hole_data.course
    return render(request, "home/hole-detail.html", {"obj": hole_data, "course": course_data})


def htmx_create_tee(request, pk):
    if request.method == "POST":
        hole = models.Hole.objects.filter(pk=pk).first()
        form = forms.TeeForm(request.POST)
        if form.is_valid():
            tee = form.save(commit=False)
            tee.hole = hole
            tee.save()
            return render(request, "home/hole-detail.html", {"obj": hole, "course": hole.course})
    else:
        form = forms.TeeForm()
    return render(request, "home/crispy-form.html", {"form": form})
