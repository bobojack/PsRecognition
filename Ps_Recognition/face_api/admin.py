from django.contrib import admin
from face_api.models import IMG


class IMGAdmin(admin.ModelAdmin):
    list_display = ('id', 'img')


admin.site.register(IMG, IMGAdmin)
# Register your models here.
