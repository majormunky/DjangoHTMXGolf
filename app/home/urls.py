from django.urls import path
from . import views


app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("golf-courses/", views.golf_courses, name="golf-courses"),
    path("golf-courses/<int:pk>/", views.golf_course_detail, name="golf-course-detail"),
    path("golf-courses/create-course/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-course"),
    path("hole/<int:pk>/", views.hole_detail, name="hole-detail"),
    path("hole/create-tee/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-tee"),
    path("hole/<int:pk>/update-par/", views.update_par_for_hole, name="update-par-for-hole"),
    path("players/", views.players, name="players"),
    path("players/<int:pk>/", views.player_detail, name="player-detail"),
    path("players/create/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-player"),
    path("games/", views.games, name="games"),
    path("games/<int:pk>/", views.game_detail, name="game-detail"),
    path("games/create/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-game"),
    path("games/<int:pk>/add-player/", views.htmx_create_players_form, name="htmx-create-player-form"),
    path("games/<int:game_pk>/remove-player/<int:player_pk>/", views.remove_player_from_game, name="remove-player-from-game"),
]
