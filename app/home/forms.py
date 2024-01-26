from django import forms
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
        
