from django.db import models
from django.utils.translation import gettext_lazy
from polymorphic.models import PolymorphicModel

class Contact(PolymorphicModel):
    IS_NUMBER = False

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy("Contact name")
    )

    order = models.IntegerField(
        verbose_name = gettext_lazy("Weight"),
        default = 0
    )

    def is_number_text(self):
        return gettext_lazy("YES") if self.IS_NUMBER else gettext_lazy(" - ")

    is_number_text.short_description =gettext_lazy("Is number ?")


    def is_number(self):
        return self.IS_NUMBER

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Contact")
        ordering  = ['order']


class ContactPortal(Contact):
    url = models.CharField(
        max_length = 1000,
        verbose_name = gettext_lazy("Contact url")
    )

    class Meta:
        verbose_name = gettext_lazy("Contact portal")

class ContactNumber(Contact):
    IS_NUMBER = True

    number = models.CharField(
        max_length = 30,
        verbose_name = gettext_lazy("Contact number")
    )

    class Meta:
        verbose_name = gettext_lazy("Contact number")