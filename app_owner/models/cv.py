from django.db import models
from django.utils.translation import gettext_lazy
from django.utils.text import slugify
from django.urls import reverse
from app_cms.utils.get_template_choices import get_templates_choices
from django.db import transaction
from nanoid import generate

class CV(models.Model):
    Templates = (
        ('test', 'test'),
    )

    slug = models.SlugField(
        verbose_name = gettext_lazy('Slug')
    )

    reset_slug = models.BooleanField(default = False)

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Version name')
    )

    template = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('PDF template'),
        blank = True,
        choices = get_templates_choices('pdf'),
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

    @property
    def url(self):
        if not self.slug:
            return ''
        return reverse('cv', kwargs={'slug': self.slug })

    def save(self):
        if self.reset_slug or not self.slug:
            hash = generate('1234567890abcdefefghijklmneoprstyuvwxyz')
            self.slug = slugify(hash)

        self.reset_slug = False
        return super(CV, self).save()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CV PDF"
        verbose_name_plural = "CV PDFs"