from django.contrib import admin
from . import models


admin.site.register(models.GolfCourse)
admin.site.register(models.Hole)
admin.site.register(models.Tee)
admin.site.register(models.Player)
admin.site.register(models.Game)
admin.site.register(models.HoleScore)
admin.site.register(models.Location)

