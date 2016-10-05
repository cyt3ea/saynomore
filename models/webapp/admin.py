from django.contrib import admin
from webapp import models

# Register your models here.
admin.site.register(models.Hair)
admin.site.register(models.User)
admin.site.register(models.Stylist)
admin.site.register(models.Review)
