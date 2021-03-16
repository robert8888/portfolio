from django.db import models
from polymorphic.models import PolymorphicModel, PolymorphicManager
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager
from parler.managers import TranslatableManager, TranslatableQuerySet
from polymorphic.query import PolymorphicQuerySet
from parler.managers import TranslatableManager
from django.utils.text import slugify
from portfolio.s3proxy import replaceImgUrl

class PropertyQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass

class PropertyManager(PolymorphicManager, TranslatableManager):
    queryset_class = PropertyQuerySet


class Property(PolymorphicModel):
    TYPE = None

    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        max_length = 255,
        default = ''
    )

    def __str__(self):
        return self.name

    def type(self):
        return self.TYPE

    def save(self):
        self.name = slugify(self.name)
        super(Property, self).save()

    class Meta:
        verbose_name = "Property"


class PropertyText(Property, TranslatableModel):
    TYPE = 'text'

    default_manager = PropertyManager()

    translations = TranslatedFields(
        value = models.CharField(
            max_length = 255,
            verbose_name = 'Text value',
            default = ''
        )
    )


    class Meta:
        verbose_name = "Property Text"


class PropertyTextLong(Property, TranslatableModel):
    TYPE = 'text_long'

    default_manager = PropertyManager()

    translations = TranslatedFields(
        value = models.TextField(
            verbose_name = 'Text value',
            default = ''
        )
    )

    class Meta:
        verbose_name = "Property Text Long"



class PropertyTextRich(Property, TranslatableModel):
    TYPE = 'text_rich'

    default_manager = PropertyManager()

    translations = TranslatedFields(
        value = models.TextField(
            verbose_name = 'Text value',
            default = ''
        )
    )

    def save(self):
        self.value = replaceImgUrl(self.value)
        super(PropertyTextRich, self).save()

    class Meta:
        verbose_name = "Property Text Rich"