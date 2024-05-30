from . import forms
from . import models


def get_form_by_slug(slug):
    form = None
    if slug == "create-tee-form":
        form = forms.TeeForm()
    elif slug == "create-course-form":
        form = forms.GolfCourseForm()
    elif slug == "create-player-form":
        form = forms.PlayerForm()
    elif slug == "create-game-form":
        form = forms.GameForm()
    return form


def create_holes_for_course(course_data):
    hole_count = int(course_data.hole_count)
    for hole in range(hole_count):
        new_hole = models.Hole(name=f"Hole: {hole + 1}", order=hole, course=course_data)
        new_hole.save()


def setup_scores_for_game(game_data):
    hole_configuration = game_data.holes_played
    links = models.PlayerGameLink.objects.filter(game=game_data)

    if hole_configuration in ["9", "18"]:
        holes = models.Hole.objects.filter(course=game_data.course).order_by("order")
    elif hole_configuration == "front-9":
        holes = models.Hole.objects.filter(
            course=game_data.course, order__lte=8
        ).order_by("order")
    elif hole_configuration == "back-9":
        holes = models.Hole.objects.filter(
            course=game_data.course, order__gte=9
        ).order_by("order")

    for hole in holes:
        for link in links:
            existing_score = models.HoleScore.objects.filter(
                hole=hole, game_link=link
            ).exists()

            if not existing_score:
                models.HoleScore.objects.create(
                    hole=hole, current_par=hole.par, score=0, game_link=link
                )
