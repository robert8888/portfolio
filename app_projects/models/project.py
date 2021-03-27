from django.db import models
from django.utils.translation import gettext_lazy
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db.models import Value
from .project_search_autocomplete import ProjectSearchAutocomplete
from .project_links import ProjectLink


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
        ),

        search_vector = SearchVectorField(null=True),

        autocomplete_hint = ArrayField(
            models.CharField(max_length = 50, verbose_name = gettext_lazy('hint')),
            verbose_name = gettext_lazy('Autocomplete hint'),
            null = True,
            blank = True
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

    def links(self):
        return ProjectLink.objects.filter(project_id = self.id)

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.title)
        technologies = ' '.join([technology.name for technology in self.technology.all()])
        self.search_vector = SearchVector(
            SearchVector('name', weight="C")
            + SearchVector('title', weight="A")
            + SearchVector('subtitle', weight="A")
            + SearchVector('autocomplete_hint', weight="A")
            + SearchVector('description_short', weight="B")
            + SearchVector(Value(technologies, models.TextField()), weight="C")
        )
        return super(Project, self).save()

    def delete(self, *args, **kwargs):
        ProjectSearchAutocomplete.objects.filter(source_id = self.id, type='project').delete()
        super(Technology, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = gettext_lazy('Project')
        verbose_name_plural = gettext_lazy('Projects')
