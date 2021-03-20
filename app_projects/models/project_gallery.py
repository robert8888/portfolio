from django.db import models
from django.utils.translation import gettext_lazy
from imagefield.fields import ImageField, PPOIField
from django.contrib.postgres.fields import ArrayField

class ProjectGallery(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Project gallery")
        verbose_name_plural = gettext_lazy("Projects gallery")
        db_table = 'app_projects_project_gallery'


class ProjectGalleryImage(models.Model):
    order = models.PositiveIntegerField(
        default = 0
    )

    gallery = models.ForeignKey(
        'ProjectGallery',
        on_delete = models.CASCADE,
    )

    image = ImageField(
        verbose_name = gettext_lazy("Image"),
        height_field = 'height',
        width_field = 'width',
        ppoi_field = 'ppoi',
        upload_to = 'project_gallery/',
        formats = {'full': ['default', ('thumbnail', (250, 180))],}
    )

    width = models.PositiveIntegerField(
        verbose_name = gettext_lazy("Image width")
    )

    height = models.PositiveIntegerField(
        verbose_name = gettext_lazy("Image height")
    )

    ppoi = PPOIField('Image PPOI')


    def __str__(self):
        return ''

    class Meta:
        verbose_name = gettext_lazy("Gallery Image")
        verbose_name_plural = gettext_lazy("Gallery Images")
        db_table = 'app_projects_project_gallery_image'
        ordering = ['order']