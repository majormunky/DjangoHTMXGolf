import pytest
from . import utils
from . import pdf_utils
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


def test_converting_holes_played_to_value():
    tests = [
        ("front-9", "9"),
        ("back-9", "9"),
        ("9", "9"),
        ("18", "18")
    ]

    for holes_played, expected_result in tests:
        actual_result = pdf_utils.convert_holes_played(holes_played)
        assert expected_result == actual_result


@pytest.mark.django_db
def test_creating_scorecard_hole_row_for_nine_hole_game(nine_hole_game):
    first_row = pdf_utils.generate_hole_row(nine_hole_game)
    assert len(first_row) == 11
    assert first_row[0] == "Hole"
    assert first_row[-1] == "Total"

    for i in range(9):
        assert first_row[i + 1] == str(i + 1)


@pytest.mark.django_db
def test_creating_scorecard_hole_row_for_eighteen_hole_game(eighteen_hole_game):
    first_row = pdf_utils.generate_hole_row(eighteen_hole_game)
    assert len(first_row) == 22
    assert first_row[0] == "Hole"
    assert first_row[10] == "Front"
    assert first_row[-1] == "Total"
    assert first_row[-2] == "Back"

    for i in range(9):
        assert first_row[i + 1] == str(i + 1)

    for i in range(10, 9):
        assert first_row[i + 1] == str(i + 1)


@pytest.mark.django_db
def test_creating_scorecard_hole_row_for_front_nine_game(eighteen_hole_game_front_nine):
    first_row = pdf_utils.generate_hole_row(eighteen_hole_game_front_nine)
    assert len(first_row) == 11
    assert first_row[0] == "Hole"
    assert first_row[-1] == "Total"

    for i in range(9):
        assert first_row[i + 1] == str(i + 1)


@pytest.mark.django_db
def test_creating_scorecard_hole_row_for_back_nine_game(eighteen_hole_game_back_nine):
    first_row = pdf_utils.generate_hole_row(eighteen_hole_game_back_nine)
    assert len(first_row) == 11
    assert first_row[0] == "Hole"
    assert first_row[-1] == "Total"

    for i in range(10, 9):
        assert first_row[i + 1] == str(i + 1)
