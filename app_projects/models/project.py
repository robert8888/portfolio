from django.db import models
from django.utils.translation import gettext_lazy
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class Project(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length = 200,
            verbose_name = gettext_lazy("Project name"),
        ),

        slug = models.SlugField(
            max_length = 255,
        ),

        title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Project title'),
        ),

        subtitle = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Project subtitle')
        ),

        description_short = models.TextField(
            verbose_name = gettext_lazy('Description short')
        ),

        description_full = models.TextField(
            verbose_name = gettext_lazy('Description long')
        )
    )

    type = models.ForeignKey(
        'ProjectType',
        on_delete = models.DO_NOTHING,
        blank = True
    )

    technology = models.ManyToManyField(
        'Technology',
        verbose_name = gettext_lazy('Technologies'),
    )

    related = models.ManyToManyField(
        'Project',
        verbose_name = gettext_lazy('Related'),
        blank = True
    )

    gallery = models.ForeignKey(
        'ProjectGallery',
        verbose_name = gettext_lazy('Gallery'),
        on_delete = models.CASCADE
    )

    release_date = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('Release date'),
        null = True
    )

    update_date = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('Last update date'),
        null = True
    )

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.title)
        return super(Project, self).save()


    class Meta:
        verbose_name = gettext_lazy('Project')
        verbose_name_plural = gettext_lazy('Projects')
