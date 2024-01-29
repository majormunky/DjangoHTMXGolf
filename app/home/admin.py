from django.contrib import admin
from . import models


admin.site.register(models.GolfCourse)
admin.site.register(models.Hole)
admin.site.register(models.Tee)
