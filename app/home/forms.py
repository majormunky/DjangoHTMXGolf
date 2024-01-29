from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from . import models


class GolfCourseForm(forms.ModelForm):
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
                "New Tee",
                "name",
                "distance"
            ),
            Submit("submit", "Submit", css_class="btn btn-primary btn-sm")
        )
        
    class Meta:
        model = models.Tee
        fields = [
            "name",
            "distance"
        ]
