from . import forms


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
