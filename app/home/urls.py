from django.urls import path
from . import views


app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("golf-courses/", views.golf_courses, name="golf-courses"),
    path("golf-courses/<int:pk>/", views.golf_course_detail, name="golf-course-detail"),
    path("golf-courses/create-course/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-course"),
    path("golf-courses/edit-course/<int:pk>/", views.htmx_edit_course_form, name="htmx-edit-course"),
    path("golf-courses/<int:pk>/detail-panel/", views.htmx_course_detail_panel, name="htmx-course-detail-panel"),
    path("golf-courses/<int:course_pk>/hole/<int:hole_pk>/", views.hole_detail, name="hole-detail"),
    path("golf-courses/<int:course_pk>/hole/<int:hole_pk>/create-tee/", views.htmx_create_tee_form, name="htmx-create-tee"),
    path("hole/<int:pk>/update-par/", views.update_par_for_hole, name="update-par-for-hole"),
    path("hole/<int:pk>/add-location/", views.ajax_add_location, name="ajax-add-location"),
    path("players/", views.players, name="players"),
    path("players/<int:pk>/", views.player_detail, name="player-detail"),
    path("players/create/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-player"),
    path("games/", views.games, name="games"),
    path("games/<int:pk>/", views.game_detail, name="game-detail"),
    path("games/<int:game_pk>/play/<int:hole_pk>/", views.play_game, name="play-game"),
    path("map-view/games/<int:game_pk>/hole/<int:hole_pk>/", views.map_view_of_hole, name="map-view"),
    path("games/create/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-game"),
    path("games/test-create/", views.htmx_create_game_form, name="htmx-create-game-form-test"),
    path("games/<int:pk>/add-player/", views.htmx_create_players_form, name="htmx-create-player-form"),
    path("games/<int:game_pk>/remove-player/<int:player_pk>/", views.htmx_remove_player_from_game, name="remove-player-from-game"),
    path("games/<int:hole_pk>/score-hole/<int:link_pk>/", views.score_hole, name="score-hole"),
    path("games/<int:pk>/start-game/", views.htmx_start_game, name="start-game"),
    path("games/<int:pk>/finish-game/", views.htmx_finish_game, name="finish-game"),
    path("games/<int:pk>/add-player-to-game/", views.htmx_add_player_to_game, name="add-player-to-game"),
    path("games/<int:game_pk>/download-scorecard/", views.download_scorecard, name="download-scorecard"),
    path("ajax/get-location-to-tee/", views.ajax_get_location_to_tee, name="ajax-get-location-to-tee"),
    path("ajax/update-location/", views.ajax_edit_location, name="ajax-edit-location"),
]
