from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from . import models


class GolfCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
    class Meta:
        model = models.GolfCourse
        fields = [
            "name",
            "hole_count",
            "tee_time_link",
            "website_link",
            "city",
            "state",
            "zip_code"
        ]


class TeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "name",
                "distance"
            )
        )
        
    class Meta:
        model = models.Tee
        fields = [
            "name",
            "distance"
        ]


class PlayerForm(forms.ModelForm):
    my_player = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "name",
                "my_player"
            )
        )

    class Meta:
        model = models.Player
        fields = [
            "name",
        ]


class GameFormCourseOnly(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "course",
            )
        )

    class Meta:
        model = models.Game
        fields = [
            "course",
        ]


class GameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "course",
                "holes_played",
                "league_game"
            )
        )

    class Meta:
        model = models.Game
        fields = [
            "course",
            "holes_played",
            "league_game",
        ]


class GameFormNineHole(forms.ModelForm):
    HOLE_CHOICES = (("9", "9 Holes"),)
    holes = forms.ChoiceField(choices=HOLE_CHOICES)
    selected_course = forms.CharField(widget = forms.HiddenInput(), required = False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "course",
                "holes",
                "league_game",
                "selected_course"
            )
        )

    class Meta:
        model = models.Game
        fields = [
            "course",
            "league_game",
        ]



class GameFormEighteenHole(forms.ModelForm):
    HOLE_CHOICES = (
        ("front-9", "Front 9"),
        ("back-9", "Back 9"),
        ("18", "18 Holes"),
    )
    holes = forms.ChoiceField(choices=HOLE_CHOICES)
    selected_course = forms.CharField(widget = forms.HiddenInput(), required = False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "course",
                "holes",
                "league_game"
                "selected_course",
            )
        )

    class Meta:
        model = models.Game
        fields = [
            "course",
            "league_game",
        ]

        

class PlayerGameLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "player",
            )
        )
        
    class Meta:
        model = models.PlayerGameLink
        fields = [
            "player"
        ]


class HoleParForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "par",
            )
        )
        
    class Meta:
        model = models.Hole
        fields = [
            "par"
        ]
