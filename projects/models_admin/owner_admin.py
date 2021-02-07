from django.contrib import admin
from solo.admin import SingletonModelAdmin
from projects.models import Portal, Owner
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class OwnerAdminFrom(forms.ModelForm):
    about_short = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 15}))
    about_full = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Owner
        fields = '__all__'

class PortalInline(admin.StackedInline):
    model = Portal

class OwnerAdmin(SingletonModelAdmin):
    list_display = ('name', 'surname')
    exclude = ('photo_width', 'photo_height')
    inlines = [PortalInline]
    form = OwnerAdminFrom
