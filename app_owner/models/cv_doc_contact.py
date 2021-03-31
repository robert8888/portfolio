from django.db import models
from django.utils.translation import gettext_lazy

class CVDocumentContactContacts(models.Model):
    document_contact = models.ForeignKey(
        'CVDocumentContact',
        on_delete = models.CASCADE
    )

    contact = models.ForeignKey(
        'Contact',
        on_delete = models.CASCADE
    )

    order = models.PositiveIntegerField(default = 0)

    class Meta:
        db_table = 'app_owner_cv_doc_contact_contacts_rel'

class CVDocumentContact(models.Model):

    id_name = models.CharField(
        verbose_name = gettext_lazy('Name'),
        max_length = 100
    )

    surname = models.CharField(
        verbose_name = gettext_lazy('Surname'),
        max_length = 100
    )

    contacts = models.ManyToManyField(
        'Contact',
        verbose_name = gettext_lazy('Contacts'),
        through = CVDocumentContactContacts
    )

    class Meta:
        verbose_name = gettext_lazy('CV Document contact')
        db_table = 'app_owner_cv_doc_contact'