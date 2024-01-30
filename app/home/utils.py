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


def setup_scores_for_game(game_data):
    links = models.PlayerGameLink.objects.filter(game=game_data)
    holes = models.Hole.objects.filter(course=game_data.course).order_by("order")

    for hole in holes:
        for link in links:
            existing_score = models.HoleScore.objects.filter(
                hole=hole, game_link=link
            ).exists()

            if not existing_score:
                hole_score = models.HoleScore.objects.create(
                    hole=hole,
                    current_par=hole.par,
                    score=0,
                    game_link=link
                )
            
