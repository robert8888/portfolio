from django.db import models
from polymorphic.models import PolymorphicModel

class Variable(PolymorphicModel):
    TYPE = None

    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        max_length = 255,
        verbose_name = 'Variable name'
    )

    def type(self):
        return self.TYPE

    class Meta:
        verbose_name = "Variable"


class VariableText(Variable):
    TYPE = 'text'

    value = models.CharField(
        max_length = 255,
        verbose_name = 'Text value',
        default = ''
    )

    class Meta:
        verbose_name = "Variable Text"


class VariableTextLong(Variable):
    TYPE = 'text_long'

    value = models.TextField(
        verbose_name = 'Text value',
        default = ''
    )

    class Meta:
        verbose_name = "Variable Text Long"



class VariableTextRich(Variable):
    TYPE = 'text_rich'

    value = models.TextField(
        verbose_name = 'Text value',
        default = ''
    )

    class Meta:
        verbose_name = "Variable Text Rich"