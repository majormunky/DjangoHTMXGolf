from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from . import utils


def index(request):
    return render(request, "home/index.html", {})


def golf_courses(request):
    course_list = models.GolfCourse.objects.all()
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
            return render(request, "home/golf-courses.html", {"course_list": course_list, "form": form})
    else:
        form = forms.GolfCourseForm()
    return render(request, "home/golf-courses.html", {"course_list": course_list, "form": form})


def golf_course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(request, "home/golf-course-detail.html", {"obj": course_data})


def hole_detail(request, pk):
    hole_data = get_object_or_404(models.Hole, pk=pk)
    course_data = hole_data.course
    tee_list = hole_data.tee_set.all()
    if request.method == "POST":
        form = forms.TeeForm(request.POST)
        if form.is_valid():
            tee = form.save(commit=False)
            tee.hole = hole_data
            tee.save()
    return render(request, "home/hole-detail.html", {"obj": hole_data, "course": course_data, "tee_list": tee_list})


@login_required
def players(request):
    player_list = models.Player.objects.filter(added_by=request.user)
    if request.method == "POST":
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            my_player = form.cleaned_data["my_player"]
            if my_player:
                player.user_account = request.user
            player.added_by = request.user
            player.save()
            
    return render(request, "home/players.html", {"player_list": player_list})


@login_required
def player_detail(request, pk):
    player_data = get_object_or_404(models.Player, pk=pk)
    return render(request, "home/player-detail.html", {"player_data": player_data})


@login_required
def games(request):
    game_list = models.Game.objects.filter(created_by=request.user)
    if request.method == "POST":
        form = forms.GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
    return render(request, "home/games.html", {"game_list": game_list})


@login_required
def game_detail(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    return render(request, "home/game-detail.html", {"game_data": game_data})


def htmx_create_form(request, form_slug):
    form = utils.get_form_by_slug(form_slug)
    return render(request, "home/crispy-form.html", {"form": form, "form_id": form_slug})
