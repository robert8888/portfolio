from django.db import models
from django.utils.translation import gettext_lazy

class CVDocumentPersonalContacts(models.Model):
    document_contact = models.ForeignKey(
        'CVDocumentPersonal',
        on_delete = models.CASCADE
    )

    contact = models.ForeignKey(
        'Contact',
        on_delete = models.CASCADE
    )

    order = models.PositiveIntegerField(default = 0)

    class Meta:
        db_table = 'app_owner_cv_doc_personal_contacts_rel'

class CVDocumentPersonal(models.Model):

    photo = models.ForeignKey(
        'CVDocumentPhoto',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Photo')
    )

    name = models.CharField(
        verbose_name = gettext_lazy('Name'),
        max_length = 100
    )

    surname = models.CharField(
        verbose_name = gettext_lazy('Surname'),
        max_length = 100
    )

    age = models.PositiveIntegerField(
        verbose_name = gettext_lazy('Age'),
        blank = True,
        null = True
    )

    contacts = models.ManyToManyField(
        'Contact',
        verbose_name = gettext_lazy('Contacts'),
        through = CVDocumentPersonalContacts
    )

    def __str__(self):
        return self.name + ' ' + self.surname


    class Meta:
        verbose_name = gettext_lazy('CV Document contact')
        db_table = 'app_owner_cv_doc_personal'