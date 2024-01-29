from django.urls import path
from . import views


app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("golf-courses/", views.golf_courses, name="golf-courses"),
    path("golf-courses/<int:pk>/", views.golf_course_detail, name="golf-course-detail"),
    path("golf-courses/create-course/", views.htmx_create_course, name="htmx-create-course"),
    path("hole/<int:pk>/", views.hole_detail, name="hole-detail"),
    path("hole/<int:pk>/create-tee/", views.htmx_create_tee, name="htmx-create-tee"),
    path("players/", views.players, name="players"),
    path("players/<int:pk>/", views.player_detail, name="player-detail"),
    path("players/create/", views.htmx_create_player, name="htmx-create-player"),
    path("games/", views.games, name="games"),
    path("games/create/<slug:form_slug>/", views.htmx_create_form, name="htmx-create-game"),
]
