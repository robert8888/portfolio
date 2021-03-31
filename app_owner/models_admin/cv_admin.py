from django.contrib import admin
from app_owner.models import (
    CV,
)

@admin.register(CV)
class CV_Admin(admin.ModelAdmin):
    pass