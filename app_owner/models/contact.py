from django.db import models
from django.utils.translation import gettext_lazy
from polymorphic.models import PolymorphicModel

class Contact(PolymorphicModel):
    IS_NUMBER = ''

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy("Contact name")
    )

    order = models.IntegerField(
        verbose_name = gettext_lazy("Weight"),
        default = 0
    )

    show_on_index = models.BooleanField(
        verbose_name = gettext_lazy("Show on main page"),
        default = True,
    )


    def type(self):
        return self.TYPE

    type.short_description =gettext_lazy("Contact type")


    def is_number(self):
        return self.TYPE

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Contact")
        ordering  = ['order']


class ContactPortal(Contact):
    TYPE = gettext_lazy('Portal')

    url = models.CharField(
        max_length = 1000,
        verbose_name = gettext_lazy("Contact url")
    )

    class Meta:
        verbose_name = gettext_lazy("Contact portal")

class ContactNumber(Contact):
    TYPE = gettext_lazy('Number')

    number = models.CharField(
        max_length = 30,
        verbose_name = gettext_lazy("Contact number")
    )

    class Meta:
        verbose_name = gettext_lazy("Contact number")

class ContactAddress(Contact):
    TYPE = gettext_lazy('Address')

    address = models.TextField(
        verbose_name = gettext_lazy('Address'),
        default = ''
    )

    class Meta:
        verbose_name = gettext_lazy('Contact address')