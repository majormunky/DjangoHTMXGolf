import pytest
from . import utils
from . import models


@pytest.mark.django_db
def test_creating_nine_hole_game_creates_correct_holescores(nine_hole_game):
    utils.setup_scores_for_game(nine_hole_game)
    game_link = models.PlayerGameLink.objects.filter(game=nine_hole_game).first()
    hole_scores = models.HoleScore.objects.filter(game_link=game_link)

    assert len(hole_scores) == 9


@pytest.mark.django_db
def test_creating_front_nine_game_creates_correct_holescores(eighteen_hole_game_front_nine):
    utils.setup_scores_for_game(eighteen_hole_game_front_nine)
    game_link = models.PlayerGameLink.objects.filter(game=eighteen_hole_game_front_nine).first()
    hole_scores = models.HoleScore.objects.filter(game_link=game_link)

    assert len(hole_scores) == 9
    assert hole_scores[8].hole.name == "Hole: 9"


@pytest.mark.django_db
def test_creating_back_nine_game_creates_correct_holescores(eighteen_hole_game_back_nine):
    utils.setup_scores_for_game(eighteen_hole_game_back_nine)
    game_link = models.PlayerGameLink.objects.filter(game=eighteen_hole_game_back_nine).first()
    hole_scores = models.HoleScore.objects.filter(game_link=game_link)

    assert len(hole_scores) == 9
    assert hole_scores[8].hole.name == "Hole: 18"


@pytest.mark.django_db
def test_creating_eighteen_hole_game_creates_correct_holescores(eighteen_hole_game):
    utils.setup_scores_for_game(eighteen_hole_game)
    game_link = models.PlayerGameLink.objects.filter(game=eighteen_hole_game).first()
    hole_scores = models.HoleScore.objects.filter(game_link=game_link)

    assert len(hole_scores) == 18

