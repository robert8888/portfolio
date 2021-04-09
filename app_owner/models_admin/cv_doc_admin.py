from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy
from app_owner.models import CVDocument, CVDocumentAdditional
from pprint import pprint
from inspect import getmembers

class CVDocumentAdditionaForm(ModelForm):
    class Meta:
        model = CVDocumentAdditional
        fields = "__all__"
        labels = {
            "cv_document_additional": gettext_lazy("Additional"),
        }

class CVDocumentAdditionalInlineAdmin(admin.StackedInline):
    extra = 0
    model = CVDocument.additional.through
    form = CVDocumentAdditionaForm
    verbose_name = gettext_lazy("Additional information")
    verbose_name_plural = gettext_lazy("Additional information")


@admin.register(CVDocument)
class CV_Admin(admin.ModelAdmin):
    exclude = ['additional']
    inlines = (CVDocumentAdditionalInlineAdmin, )
    pass