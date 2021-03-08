from django.contrib import admin
from django import forms

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

class TechnologyAdminFrom(forms.ModelForm):
    is_main = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select(), initial = '')

class TechnologyAdmin(admin.ModelAdmin):
    exclude = ['logo_width', 'logo_height']
    form = TechnologyAdminFrom