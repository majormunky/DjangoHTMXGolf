import collections
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from . import models
from . import forms
from . import utils
from . import pdf_utils


def index(request):
    return render(request, "home/index.html", {})


def about(request):
    return render(request, "home/about.html", {})


def golf_courses(request):
    course_list = models.GolfCourse.objects.all()
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST)
        if form.is_valid():
            course_data = form.save()
            utils.create_holes_for_course(course_data)
            return render(
                request,
                "home/golf-courses.html",
                {"course_list": course_list, "form": form},
            )
    else:
        form = forms.GolfCourseForm()
    return render(
        request, "home/golf-courses.html", {"course_list": course_list, "form": form}
    )


def golf_course_detail(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    front_holes = models.Hole.objects.filter(course=course_data, order__lte=8)
    back_holes = models.Hole.objects.filter(course=course_data, order__gte=9)
    if request.method == "POST":
        form = forms.GolfCourseForm(request.POST, instance=course_data)
        if form.is_valid():
            form.save()
            return render(
                request, "home/fragments/course-detail-panel.html", {"obj": course_data, "front_holes": front_holes, "back_holes" : back_holes}
            )
    return render(request, "home/golf-course-detail.html", {"obj": course_data, "front_holes": front_holes, "back_holes" : back_holes})


def hole_detail(request, course_pk, hole_pk):
    hole_data = get_object_or_404(models.Hole, pk=hole_pk)
    course_data = hole_data.course
    tee_list = hole_data.tee_set.all()
    hole_form = forms.HoleParForm(instance=hole_data)
    location_form = forms.LocationForm()
    location_list = models.Location.objects.filter(hole=hole_data)
    if request.method == "POST":
        form = forms.TeeForm(request.POST)
        if form.is_valid():
            tee = form.save(commit=False)
            tee.hole = hole_data
            tee.save()
    return render(
        request,
        "home/hole-detail.html",
        {
            "obj": hole_data,
            "course": course_data,
            "tee_list": tee_list,
            "par_form": hole_form,
            "location_form": location_form,
            "location_list": location_list
        },
    )


@login_required
def update_par_for_hole(request, pk):
    hole_data = get_object_or_404(models.Hole, pk=pk)
    if request.method == "POST":
        form = forms.HoleParForm(request.POST)
        if form.is_valid():
            new_par_value = form.cleaned_data["par"]
            hole_data.par = new_par_value
            hole_data.save()
    return render(request, "home/par-info.html", {"obj": hole_data})


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
    game_links = (
        models.PlayerGameLink.objects.filter(player=player_data)
        .select_related("player", "game", "game__course")
        .order_by("-game__date_played")
    )
    return render(
        request,
        "home/player-detail.html",
        {"player_data": player_data, "game_link_list": game_links},
    )


@login_required
def games(request):
    game_list = models.Game.objects.filter(created_by=request.user).order_by("-date_played")
    form = forms.GameForm()
    if request.method == "POST":
        selected_course = request.POST.get("selected_course", None)
        holes = request.POST.get("holes", None)
        league_game = request.POST.get("league_game", False)
        if league_game == "on":
            league_game = True

        if all([selected_course, holes]):
            course_data = models.GolfCourse.objects.filter(pk=selected_course).first()
            new_game = models.Game.objects.create(
                course=course_data,
                holes_played=holes,
                league_game=league_game,
                created_by=request.user,
            )
    else:
        form = forms.GameFormCourseOnly()
    return render(request, "home/games.html", {"game_list": game_list, "form": form})


@login_required
def game_detail(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    player_links = models.PlayerGameLink.objects.filter(game=game_data)

    front_hole_list = models.Hole.objects.filter(course=game_data.course, order__lte=8).order_by("order")
    back_hole_list = models.Hole.objects.filter(course=game_data.course, order__gte=9).order_by("order")

    first_hole_score = (
        models.HoleScore.objects.filter(hole__course=game_data.course)
        .order_by("hole__order")
        .first()
    )

    front_score_list = (
        models.HoleScore.objects.filter(hole__course=game_data.course, game_link__game=game_data, hole__order__lte=8)
        .order_by("hole__order")
    )

    back_score_list = (
        models.HoleScore.objects.filter(hole__course=game_data.course, game_link__game=game_data, hole__order__gte=9)
        .order_by("hole__order")
    )

    score_data = {
        "header": {
            "front": [],
            "back": []
        },
        "rows": {
            "front": [],
            "back": []
        }
    }

    active_tab = "front"
    if game_data.holes_played == "back-9":
        active_tab = "back"

    if game_data.holes_played in ["9", "front-9", "18"]:
        front_hole_row = ["Hole"]
        for hole in front_hole_list:
            front_hole_row.append(hole.order + 1)
        front_hole_row.append("Total")
        score_data["header"]["front"] = front_hole_row

    if game_data.holes_played in ["back-9", "18"]:
        back_hole_row = ["Hole"]
        for hole in back_hole_list:
            back_hole_row.append(hole.order + 1)
        back_hole_row.append("Total")
        score_data["header"]["back"] = back_hole_row

    player_scores = {"front": {}, "back": {}}

    for player in player_links:
        player_scores["front"][player.player.name] = []
        player_scores["back"][player.player.name] = []

    for front_score in front_score_list:
        player_scores["front"][front_score.game_link.player.name].append(front_score.score)

    for back_score in back_score_list:
        player_scores["back"][back_score.game_link.player.name].append(back_score.score)

    for course_pos in ["front", "back"]:
        for player_name, score_list in player_scores[course_pos].items():
            player_row = [player_name] + score_list
            player_row.append(sum(score_list))
            score_data["rows"][course_pos].append(player_row)

    return render(
        request,
        "home/game-detail.html",
        {
            "game_data": game_data,
            "player_links": player_links,
            "first_hole_score": first_hole_score,
            "score_data": score_data,
            "active_tab": active_tab
        },
    )


@login_required
def map_view_of_hole(request, game_pk, hole_pk):
    hole_data = get_object_or_404(models.Hole, pk=hole_pk)
    game_data = get_object_or_404(models.Game, pk=game_pk)
    return render(request, "home/map-view.html", {"game_data": game_data, "hole_data": hole_data})


@login_required
def play_game(request, game_pk, hole_pk):
    hole_data = get_object_or_404(models.Hole, pk=hole_pk)
    game_data = get_object_or_404(models.Game, pk=game_pk)
    # hole_score_data = get_object_or_404(models.HoleScore, pk=hole_score_pk)
    # hole_score_data = models.HoleScore.objects.filter(hole=hole_data, game_link__game=game_data)

    hole_list = game_data.get_holes()

    prev_hole_score = models.HoleScore.objects.filter(
        hole__course=game_data.course,
        hole__order=hole_data.order - 1,
        game_link__game=game_data,
    ).first()
    next_hole_score = models.HoleScore.objects.filter(
        hole__course=game_data.course,
        hole__order=hole_data.order + 1,
        game_link__game=game_data,
    ).first()

    hole_scores = models.HoleScore.objects.filter(
        hole=hole_data,
        game_link__game=game_data
    )
    return render(
        request,
        "home/play-game.html",
        {
            "game_data": game_data,
            "hole_data": hole_data,
            "hole_scores": hole_scores,
            "prev_hole_score": prev_hole_score,
            "next_hole_score": next_hole_score,
            "hole_list": hole_list,
            "current_hole_pk": hole_pk
        },
    )


@login_required
def score_hole(request, hole_pk, link_pk):
    if request.method == "POST":
        hole_score_data = models.HoleScore.objects.filter(pk=hole_pk).first()
        score = request.POST.get("score")
        hole_score_data.score = int(score)
        hole_score_data.save()

        return HttpResponse("success")


@login_required
def download_scorecard(request, game_pk):
    game_data = get_object_or_404(models.Game, pk=game_pk)
    pdf_data = pdf_utils.generate_scorecard(game_data)
    response = HttpResponse(pdf_data.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=scorecard.pdf'
    return response


@login_required
def htmx_remove_player_from_game(request, player_pk, game_pk):
    player_data = models.Player.objects.filter(pk=player_pk).first()
    game_data = models.Game.objects.filter(pk=game_pk).first()
    game_link = models.PlayerGameLink.objects.filter(
        game=game_data, player=player_data
    ).first()

    game_link.delete()

    player_links = models.PlayerGameLink.objects.filter(game=game_data)

    return render(
        request,
        "home/fragments/game-player-table.html",
        {"game_data": game_data, "player_links": player_links},
    )


@login_required
def htmx_add_player_to_game(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    player_links = models.PlayerGameLink.objects.filter(game=game_data)
    if request.method == "POST":
        form = forms.PlayerGameLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.game = game_data
            link.save()
            # normally when starting a game we setup the scores
            # but if a player is added late, we add them when
            # a player is added
            if game_data.status == "active":
                utils.setup_scores_for_game(game_data)
        return render(
            request,
            "home/fragments/game-player-table.html",
            {"game_data": game_data, "player_links": player_links}
        )


@login_required
def htmx_start_game(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    game_data.start()
    utils.setup_scores_for_game(game_data)
    first_hole_score = (
        models.HoleScore.objects.filter(hole__course=game_data.course)
        .order_by("hole__order")
        .first()
    )
    return render(request, "home/fragments/game-detail-panel.html", {"game_data": game_data, "first_hole_score": first_hole_score})


@login_required
def htmx_finish_game(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    game_data.finish()
    return render(request, "home/fragments/game-detail-panel.html", {"game_data": game_data})


@login_required
def htmx_create_players_form(request, pk):
    game_data = get_object_or_404(models.Game, pk=pk)
    existing_player_links = models.PlayerGameLink.objects.filter(game=game_data)
    existing_players = []
    for link in existing_player_links:
        existing_players.append(link.player.id)

    form_queryset = models.Player.objects.filter(added_by=request.user).exclude(
        id__in=existing_players
    )
    form = forms.PlayerGameLinkForm()
    form.fields["player"].queryset = form_queryset
    return render(
        request,
        "home/fragments/add-player-to-game-form.html",
        {"form": form, "game_data": game_data},
    )


@login_required
def htmx_create_game_form(request):
    selected_course = request.GET.get("course", None)
    if selected_course:
        course_data = get_object_or_404(models.GolfCourse, pk=selected_course)
        if course_data.hole_count == "9":
            form = forms.GameFormNineHole(
                initial={"course": course_data, "selected_course": selected_course}
            )
        else:
            form = forms.GameFormEighteenHole(
                initial={"course": course_data, "selected_course": selected_course}
            )
        form.fields["course"].disabled = True
    else:
        form = forms.GameFormCourseOnly()
    return render(
        request, "home/crispy-form.html", {"form": form, "form_id": "game-form"}
    )


def htmx_create_form(request, form_slug):
    form = utils.get_form_by_slug(form_slug)
    return render(
        request, "home/crispy-form.html", {"form": form, "form_id": form_slug}
    )


@login_required
def htmx_edit_course_form(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    form = forms.GolfCourseForm(instance=course_data)
    return render(
        request,
        "home/fragments/edit-course-form.html",
        {"form": form, "obj": course_data},
    )


@login_required
def htmx_course_detail_panel(request, pk):
    course_data = get_object_or_404(models.GolfCourse, pk=pk)
    return render(
        request,
        "home/fragments/course-detail-panel.html",
        {"obj": course_data},
    )


@login_required
def htmx_create_tee_form(request, course_pk, hole_pk):
    form = utils.get_form_by_slug("create-tee-form")
    return render(
        request, "home/crispy-form.html", {"form": form, "form_id": "create-tee-form"}
    )


@login_required
def ajax_add_location(request, pk):
    if request.method != "POST":
        return JsonResponse({"status": "failed"}, status_code=405)
    data = json.loads(request.body)
    name = data.get("name", None)
    long = data.get("longitude", None)
    lat = data.get("latitude", None)
    if not all([name, long, lat]):
        return JsonResponse({"status": "failed", "message": "Missing Data"})
    hole_data = models.Hole.objects.filter(pk=pk).first()
    if hole_data is None:
        return JsonResponse({"status": "failed", "message": "Unable to find hole"}, status_code=400)
    existing_location = models.Location.objects.filter(hole=hole_data, name=name).exists()
    if existing_location:
        return JsonResponse({"status": "failed", "message": "Location already exists"}, status_code=406)
    new_location = models.Location.objects.create(
        name=name,
        longitude=long,
        latitude=lat,
        hole=hole_data
    )
    return JsonResponse({"status": "success"})


@login_required
def ajax_edit_location(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed"}, status_code=405)
    data = json.loads(request.body)
    long = data.get("longitude", None)
    lat = data.get("latitude", None)
    pk = data.get("location_id", None)
    if not all([long, lat, pk]):
        return JsonResponse({"status": "failed", "message": "Missing Data"})
    location_data = models.Location.objects.filter(pk=pk).first()
    if location_data is None:
        return JsonResponse({"status": "failed", "message": "Unable to find location"}, status_code=400)
    location_data.longitude = long
    location_data.latitude = lat
    location_data.save()

    return JsonResponse({"status": "success"})



@login_required
def ajax_get_location_to_tee(request):
    data = json.loads(request.body)
    hole_pk = data.get("hole_pk", 0)
    hole_data = models.Hole.objects.filter(pk=hole_pk).first()
    if hole_data is None:
        return JsonResponse({"status": "failed", "message": "Unable to find hole"})

    pin_location = models.Location.objects.filter(hole=hole_data, name="pin").first()
    if pin_location is None:
        return JsonResponse({
            "status": "failed",
            "message": "No Pin Location for this hole"
        })

    long = data.get("longitude", None)
    lat = data.get("latitude", None)
    if not all([long, lat]):
        return JsonResponse({"status": failed})
    dist = utils.get_distance_between_points(
        (float(pin_location.latitude), float(pin_location.longitude)),
        (lat, long)
    )
    return JsonResponse({"status": "success", "yards": dist["yards"]})
