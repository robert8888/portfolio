from django.db import models
from django.utils.translation import gettext_lazy
from polymorphic.models import PolymorphicModel
import phonenumbers
import re

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

    protected = models.BooleanField(
        verbose_name = gettext_lazy('Contact protected'),
        default = False,
    )

    def type(self):
        return self.TYPE

    type.short_description = gettext_lazy("Contact type")


    def value(self):
        return ''

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

    def value(self):
        return self.url


    def value_display(self):
        return re.sub('mailto:|https?://', '', self.url)


    class Meta:
        verbose_name = gettext_lazy("Contact portal")

class ContactEmail(Contact):
    TYPE = gettext_lazy('Email')

    email = models.CharField(
        max_length = 100,
        verbose_name = gettext_lazy('Email address')
    )

    def value(self):
        return self.email

    def value_display(self):
        return re.sub('mailto:|https?://', '', self.email)

    class Meta:
        verbose_name = gettext_lazy('Contact email')


class ContactNumber(Contact):
    TYPE = gettext_lazy('Number')

    number = models.CharField(
        max_length = 30,
        verbose_name = gettext_lazy("Contact number")
    )

    def value(self):
        return self.number

    def value_display(self):
        try:
            return phonenumbers.format_number(
                phonenumbers.parse(self.number, None),
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        except BaseException as error:
            self.number


    class Meta:
        verbose_name = gettext_lazy("Contact number")

class ContactAddress(Contact):
    TYPE = gettext_lazy('Address')

    address = models.TextField(
        verbose_name = gettext_lazy('Address'),
        default = ''
    )

    def value(self):
        return self.address

    def value_display(self):
        return self.address

    class Meta:
        verbose_name = gettext_lazy('Contact address')