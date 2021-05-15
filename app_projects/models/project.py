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
from sortedm2m.fields import SortedManyToManyField
from django.utils.translation import get_language
from django.conf import settings
import re

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

        meta_title = models.CharField(
            max_length=55,
            blank = True,
            null = True,
            verbose_name=gettext_lazy('Project page meta title')
        ),

        meta_description = models.CharField(
            max_length=255,
            blank = True,
            null = True,
            verbose_name=gettext_lazy('Project page meta description')
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
        ),

        json_ld=models.JSONField(
            verbose_name="Json ld",
            blank=True,
            null=True
        )
    )

    application_cat = models.CharField(
        max_length=100,
        choices=[
            (type, ' '.join(re.findall('[A-Z][^A-Z]*', type)))
            for type in sorted([
                'GameApplication',
                'SocialNetworkingApplication',
                'TravelApplication',
                'ShoppingApplication',
                'SportsApplication',
                'LifestyleApplication',
                'BusinessApplication',
                'DesignApplication',
                'DeveloperApplication',
                'DriverApplication',
                'EducationalApplication',
                'HealthApplication',
                'FinanceApplication',
                'SecurityApplication',
                'BrowserApplication',
                'CommunicationApplication',
                'DesktopEnhancementApplication',
                'EntertainmentApplication',
                'MultimediaApplication',
                'HomeApplication',
                'UtilitiesApplication',
                'ReferenceApplication'
            ], key=str.lower)
        ],
        null=True,
        blank=True,
        default = 'UtilitiesApplication',
        verbose_name='Seo app category'
    )

    operating_system = models.CharField(
        max_length=255,
        choices=[
            (system, system) for system in [
                'Unix',
                'Windows',
                'OSX',
                'Android',
                'Any'
            ]
        ],
        default='Any',
        verbose_name='SEO operating system'
    )

    type = models.ForeignKey(
        'ProjectType',
        on_delete = models.DO_NOTHING,
        blank = True
    )

    technology = SortedManyToManyField(
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

    show_on_index = models.BooleanField(
        verbose_name = gettext_lazy('Show on main page'),
        default = False
    )

    sort_weight = models.PositiveIntegerField(
        verbose_name = gettext_lazy('Default sort weight'),
        default = 0
    )

    def links(self):
        return ProjectLink.objects.filter(project_id = self.id)

    def link(self, type):
        link_queryset = ProjectLink.objects.filter(project_id = self.id, type = type)
        if not len(link_queryset):
            return ""
        urls = link_queryset[0].url
        if not len(urls):
            return ""
        return urls[0]

    @property
    def repo_link(self):
        return self.link('repo')

    @property
    def host_link(self):
        return self.link('host')

    @property
    def structured_data(self):
        return {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name" : self.name,
            "targetProduct": self.name,
            "operatingSystem": self.operating_system,
            "image" : self.gallery.images[0].image.thumb,
            "abstract": self.meta_description,
            "applicationCategory": self.application_cat,
            "author" : {
                "@type" : "Person",
                "name" : "Robert Kaminski"
            },
            "datePublished" : self.release_date.strftime("%Y-%M-%d"),
            "codeRepository" : self.repo_link,
            "codeSampleType": self.host_link,
            "programmingLanguage": self.technologies_str_by_type('Language'),
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "5",
                "ratingCount": "1"
            },
            "offers": {
                "@type": "Offer",
                "price": "0"
            }
        }

    def update_json_ld(self):
        languages = [lang[0] for lang in settings.LANGUAGES]
        for lang in languages:
            self.set_current_language(lang)
            self.json_ld = self.structured_data

        self.save()

    @property
    def technologies_str(self):
        return ' '.join([technology.name for technology in self.technology.all()]) if self.id else ''

    def technologies_str_by_type(self, type = "Language"):
        return ' '.join([technology.name for technology in self.technology.filter(type__translation__name = type)]) if self.id else ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        technologies = self.technologies_str
        translations = len(self.translations.filter(language_code = get_language())) if self.id else None
        if self.id and translations:
            self.search_vector = SearchVector(
                SearchVector('name', weight="C")
                + SearchVector('title', weight="A")
                + SearchVector('subtitle', weight="A")
                + SearchVector('autocomplete_hint', weight="A")
                + SearchVector('description_short', weight="B")
                + SearchVector(Value(technologies, models.TextField()), weight="C")
            )
        self.json_ld = self.structured_data
        return super(Project, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ProjectSearchAutocomplete.objects.filter(source_id = self.id, type='project').delete()
        super(Project, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Project')
        verbose_name_plural = gettext_lazy('Projects')
        ordering = ['sort_weight']
