from django.contrib import admin
from parler.admin import TranslatableModelForm, TranslatableAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget

from app_owner.models import (
    CVDocumentAdditional,
)


class CVDocumentAdditionalFrom(TranslatableModelForm):
    class Meta:
        model = CVDocumentAdditional
        fields = '__all__'
        widgets = {
            'items': DynamicArrayTextareaWidget(attrs={'cols': 50, 'rows': 2})
        }

@admin.register(CVDocumentAdditional)
class CVDocumentSummaryAdmin(TranslatableAdmin, DynamicArrayMixin):
    def has_module_permission(self, request): return False
    form = CVDocumentAdditionalFrom
    pass