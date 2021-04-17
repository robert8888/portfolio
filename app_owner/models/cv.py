from django.db import models
from django.utils.translation import gettext_lazy
from django.utils.text import slugify
from django.urls import reverse
from app_cms.utils.get_template_choices import getTemplatesChoices
from django.db import transaction

class CV(models.Model):
    Templates = (
        ('test', 'test'),
    )

    slug = models.SlugField(
        verbose_name = gettext_lazy('Slug')
    )

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Version name')
    )

    template = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('PDF template'),
        blank = True,
        choices = getTemplatesChoices('pdf'),
    )

    color_profile = models.ForeignKey(
        'CVColorProfile',
        on_delete = models.RESTRICT,
    )

    data = models.ForeignKey(
        'CVDocument',
        on_delete = models.RESTRICT,
        null = True,
        blank = True
    )

    on_main_page = models.BooleanField(
        default = False,
        verbose_name = gettext_lazy('Link on main page')
    )

    @property
    def url(self):
        if not self.slug:
            return ''
        return reverse('cv', kwargs={'slug': self.slug })

    def save(self):
        self.slug = slugify(self.name)
        if self.on_main_page:
            with transaction.atomic():
                CV.objects.filter(on_main_page = True).update(on_main_page = False)

        return super(CV, self).save()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CV PDF"
        verbose_name_plural = "CV PDFs"