from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from sortedm2m.fields import SortedManyToManyField


class CVDocument_additional(models.Model):
    cv_document = models.ForeignKey('CVDocument',on_delete=models.CASCADE)
    cv_document_additional = models.ForeignKey('CVDocumentAdditional',on_delete=models.CASCADE)
    def __str__(self):
        return ''
    class Meta:
        verbose_name = gettext_lazy('Additional information')

class CVDocument(models.Model):

    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    on_main_page = models.BooleanField(
        default = False,
        verbose_name = gettext_lazy('Link on main page')
    )

    document_title = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Document title'),
        blank = True,
        help_text = gettext_lazy('If not present default: Name + Surname')
    )

    download_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Document download filename'),
        blank = True,
        help_text = gettext_lazy('If not present default: Name + Surname')
    )

    personal = models.ForeignKey(
        'CVDocumentPersonal',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Personal'),
        blank = True,
        null = True,
    )

    contact = models.ForeignKey(
        'CVDocumentContact',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Contact')
    )

    summary = models.ForeignKey(
        'CVDocumentSummary',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Summary')
    )

    education = models.ForeignKey(
        'CVDocumentEducation',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Education')
    )

    experience = models.ForeignKey(
        'CVDocumentExperience',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Experience')
    )

    skills = models.ForeignKey(
        'CVDocumentSkills',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Skills')
    )

    agreements = models.ForeignKey(
        'CVDocumentAgreements',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Rodo agreements'),
        null = True,
        blank = True
    )

    additional = models.ManyToManyField(
        'CVDocumentAdditional',
        verbose_name = gettext_lazy('Additional'),
        through = CVDocument_additional
    )

    def __getattribute__(self, attr):
        if attr.startswith('additional_'):
            type = attr[11:]
            additional_queryset = CVDocument_additional.objects.filter(cv_document = self.id, cv_document_additional__type = type)
            if len(additional_queryset):
                return additional_queryset[0].cv_document_additional
            return []
        return super(CVDocument, self).__getattribute__(attr)

    @property
    def get_download_name(self):
        if not self.download_name and not self.personal:
            return 'cv'
        elif not self.download_name:
            return self.personal.name + "_" + self.personal.surname
        else:
            return self.download_name

    @property
    def get_document_title(self):
        if not self.document_title and not self.personal:
            return 'cv'
        elif not self.document_title:
            return self.personal.name + ' ' + self.personal.surname
        else:
            return self.document_title

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('CV Document')
        verbose_name_plural = gettext_lazy('CV Documents')
        db_table = 'app_owner_cv_doc'


