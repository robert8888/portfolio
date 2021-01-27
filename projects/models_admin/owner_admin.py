from django.contrib import admin
from solo.admin import SingletonModelAdmin
from django import forms
from projects.models import Portal
import inspect


class PortalInline(admin.StackedInline):
    model = Portal

class OwnerAdmin(SingletonModelAdmin):
    list_display = ('name', 'surname')
    inlines = [PortalInline]
