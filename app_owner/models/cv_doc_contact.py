from django.db import models
from django.utils.translation import gettext_lazy
from parler.models import TranslatableModel,TranslatedFields

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
        ordering = ('order',)

class CVDocumentContact(TranslatableModel):

    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    translation = TranslatedFields(
        section_name = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Contact section title'),
            default = 'Contact'
        )
    )

    contacts = models.ManyToManyField(
        'Contact',
        verbose_name = gettext_lazy('Contacts'),
        through = CVDocumentContactContacts
    )

    @property
    def contacts_ordered(self):
        return CVDocumentContactContacts.objects.filter(document_contact=self.id)

    @property
    def contacts_ordered_dict(self):
        contacts_list = CVDocumentContactContacts.objects.filter(document_contact=self.id)
        contacts = {}
        for contact_rel in contacts_list:
            contacts[contact_rel.contact.name.lower()] = contact_rel.contact
        return contacts

    def __str__(self):
        return self.id_name


    class Meta:
        verbose_name = gettext_lazy('CV Document contact')
        db_table = 'app_owner_cv_doc_contact'