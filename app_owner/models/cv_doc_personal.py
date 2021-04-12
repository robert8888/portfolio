from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy

class CVDocumentPersonal(TranslatableModel):

    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    photo = models.ForeignKey(
        'CVDocumentPhoto',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Photo')
    )

    translation = TranslatedFields(
        name = models.CharField(
            verbose_name = gettext_lazy('Name'),
            max_length = 100
        ),

        surname = models.CharField(
            verbose_name = gettext_lazy('Surname'),
            max_length = 100
        ),

        birthday = models.DateField(
            verbose_name = gettext_lazy('Birthday'),
            auto_now = False,
            null = True,
        ),

        position_title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Position title')
        ),
    )

    @property
    def full_name(self):
        return self.name + ' ' + self.surname

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('CV Document personal')
        db_table = 'app_owner_cv_doc_personal_data'