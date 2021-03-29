from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from app_projects.models.technology import Technology

class CvDocumentSkills():

    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        verbose_name = gettext_lazy("Identification name"),
        max_length = 100
    )

    technologies = ManyToManyField(
        Technology,
        verbose_name = gettext_lazy('Technology')
        verbose_name_plural = gettext_lazy('Technologies')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Document skills')
        verbose_name_plural = gettext_lazy('Documents skills')


class CvSkill(PolymorphicModel):
    document_skills = models.ForeignKey(
       'CvDocumentSkills',
       on_delete = models.CASCADE
    )

    class Meta:
        verbose_name = gettext_lazy('Skill')

class CvSkillLanguage(CvSkill):
    name = models.CharField(
        max_length = 100,
        verbose_name = gettext_lazy('Language name')
    )

    Levels = (
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
        ('c2', 'C2'),
    )

    level = models.CharField(
        max_length = 50,
        verbose_name = gettext_lazy('Level'),
        choices = Levels
    )


class CvSkillOther(TranslatableModel, CvSkill):

    translations = TranslatedFields(
        text = models.TextField(
            verbose_name = gettext_lazy('Text')
        )
    )

    level = models.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        verbose_name = gettext_lazy('Level')
    )

    class Meta:
        verbose_name = gettext_lazy('Skill')
        verbose_name_plural = gettext_lazy('Skills')