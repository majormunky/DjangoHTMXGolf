import pytest
from django.contrib.auth import get_user_model
from home import models
from home import utils


@pytest.fixture
def nine_hole_golf_course():
    course = models.GolfCourse.objects.create(
        name="Test Course",
        hole_count="9"
    )
    utils.create_holes_for_course(course)
    return course


@pytest.fixture
def eighteen_hole_golf_course():
    course = models.GolfCourse.objects.create(
        name="Test Course",
        hole_count="18"
    )
    utils.create_holes_for_course(course)
    return course


@pytest.fixture
def normal_user():
    return get_user_model().objects.create(
        username="normaluser",
        email="normal@example.com",
        password="testpass123"
    )


@pytest.fixture
def player_one(normal_user):
    return models.Player.objects.create(
        name="Player One",
        added_by=normal_user
    )


@pytest.fixture
def nine_hole_game(nine_hole_golf_course, normal_user, player_one):
    game = models.Game.objects.create(
        course=nine_hole_golf_course,
        holes_played="9",
        created_by=normal_user
    )
    game.players.add(player_one)
    return game


@pytest.fixture
def eighteen_hole_game_front_nine(eighteen_hole_golf_course, normal_user, player_one):
    game = models.Game.objects.create(
        course=eighteen_hole_golf_course,
        holes_played="front-9",
        created_by=normal_user
    )
    game.players.add(player_one)
    return game


@pytest.fixture
def eighteen_hole_game_back_nine(eighteen_hole_golf_course, normal_user, player_one):
    game = models.Game.objects.create(
        course=eighteen_hole_golf_course,
        holes_played="back-9",
        created_by=normal_user
    )
    game.players.add(player_one)
    return game


@pytest.fixture
def eighteen_hole_game(eighteen_hole_golf_course, normal_user, player_one):
    game = models.Game.objects.create(
        course=eighteen_hole_golf_course,
        holes_played="18",
        created_by=normal_user
    )
    game.players.add(player_one)
    return game


@pytest.fixture
def authenticated_client(client, normal_user):
    client.force_login(normal_user)
    return client

