from django.db import models
from django.utils.translation import gettext_lazy
from polymorphic.models import PolymorphicModel
from parler.models import TranslatableModel, TranslatedFields
from .project_search_autocomplete import ProjectSearchAutocomplete
from django.core.validators import MinValueValidator, MaxValueValidator

class Technology(models.Model):
    type = models.ForeignKey(
        'TechnologyType',
        on_delete = models.DO_NOTHING
    )

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Technology name')
    )

    link = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Technology link')
    )

    color = models.CharField(
        max_length = 36,
        verbose_name = gettext_lazy('Color')
    )

    skill_level = models.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name = gettext_lazy('Skill level'),
        default = 0
    )

    show_on_index = models.BooleanField(
        default = False,
        verbose_name = gettext_lazy('Show on main page')
    )

    show_on_index_all = models.BooleanField(
        default = False,
        verbose_name = gettext_lazy('Show on main page in all section')
    )

    def delete(self, *args, **kwargs):
        ProjectSearchAutocomplete.objects.filter(source_id = self.id, type='technology').delete()
        super(Technology, self).delete(*args, **kwargs)

    def skill_level_percentage(self):
        return str(self.skill_level * 10) + '%'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Technology')
        verbose_name_plural = gettext_lazy('Technologies')

class TechnologyType(TranslatableModel):
    translation = TranslatedFields(
        name = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Name')
        )
    )

    weight = models.IntegerField(
        default = 0,
        verbose_name = gettext_lazy('Weight')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Technology type')
        verbose_name_plural = gettext_lazy('Technology types')

class TechnologyImage(PolymorphicModel):
    image = models.ForeignKey(
        'Image',
        on_delete=models.CASCADE,
    )

    technology = models.OneToOneField(
        'Technology',
        on_delete=models.CASCADE,
    )

class TechnologyImageStd(TechnologyImage):
    class Meta:
        verbose_name = gettext_lazy('Technology image')

class TechnologyImageSprite(TechnologyImage):
    top = models.DecimalField(
        verbose_name = gettext_lazy("Top"),
        max_digits=10,
        decimal_places=2
    )

    left = models.DecimalField(
        verbose_name = gettext_lazy("Left"),
        max_digits=10,
        decimal_places=2
    )

    width = models.DecimalField(
        verbose_name = gettext_lazy("Width"),
        max_digits=10,
        decimal_places=2
    )

    height = models.DecimalField(
        verbose_name = gettext_lazy("Height"),
        max_digits=10,
        decimal_places=2
    )

class Image(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy("Image identification name")
    )

    source = models.ImageField(
        upload_to = 'portals',
        width_field = 'width',
        height_field = 'height'
    )

    width = models.PositiveIntegerField()

    height = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Image")