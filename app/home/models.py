from django.db import models


HOLE_CHOICES = (
    ("9", "9 Holes"),
    ("18", "18 Holes"),
)


class GolfCourse(models.Model):
    name = models.CharField(max_length=128)
    hole_count = models.CharField(
        max_length=64, choices=HOLE_CHOICES, default=HOLE_CHOICES[0][0]
    )
    tee_time_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    zip_code = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class Hole(models.Model):
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=128, blank=True)
    par = models.IntegerField(default=3)
    order = models.IntegerField(default=0)
    course = models.ForeignKey(GolfCourse, on_delete=models.CASCADE)
