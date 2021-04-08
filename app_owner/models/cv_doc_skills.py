from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from app_projects.models.technology import Technology
from polymorphic.models import PolymorphicModel, PolymorphicManager
from parler.managers import TranslatableManager, TranslatableQuerySet
from polymorphic.query import PolymorphicQuerySet
from sortedm2m.fields import SortedManyToManyField

class CVDocumentSkills(models.Model):

    id_name = models.CharField(
        verbose_name = gettext_lazy("Identification name"),
        max_length = 100
    )

    technologies = SortedManyToManyField(
        Technology,
        verbose_name = gettext_lazy('Technologies')
    )

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('Document skills')
        verbose_name_plural = gettext_lazy('Documents skills')
        db_table = 'app_owner_cv_doc_skills'



class CVDocumentSkill(PolymorphicModel):
    document_skills = models.ForeignKey(
       'CVDocumentSkills',
       on_delete = models.CASCADE
    )

    class Meta:
        verbose_name = gettext_lazy('Skill')
        db_table = 'app_owner_cv_doc_skill'


class CVSkillQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass

class CVSkillManager(PolymorphicManager, TranslatableManager):
    queryset_class = CVSkillQuerySet

class CVDocumentSkillLanguage(CVDocumentSkill, TranslatableModel):
    default_manager = CVSkillManager()

    translations = TranslatedFields(
        name = models.CharField(
            max_length = 100,
            verbose_name = gettext_lazy('Language name')
        )
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Language')
        verbose_name_plural = gettext_lazy('Languages')
        db_table = 'app_owner_cv_doc_skill_lang'

class CVDocumentSkillOther(CVDocumentSkill, TranslatableModel):

    default_manager = CVSkillManager()

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

    def __str__(self):
        return self.text[:25]

    class Meta:
        verbose_name = gettext_lazy('Skill')
        verbose_name_plural = gettext_lazy('Skills')
        db_table = 'app_owner_cv_doc_skill_other'

