from django.db import models
from django.utils.translation import gettext_lazy
from imagefield.fields import ImageField, PPOIField
from imagefield.processing import register


def def_processor_spec(fieldfile, context):
    context.processors = [
        "autorotate",
        "process_jpeg",
        'process_png',
        'preserve_icc_profile',
        ("thumbnail", (250, 180)),
    ]

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
        formats = {
            'thumb': ['default', ('thumbnail', (250, 180))],
            'full': ['default',]
        }
    )

    width = models.PositiveIntegerField(
        verbose_name = gettext_lazy("Image width")
    )

    height = models.PositiveIntegerField(
        verbose_name = gettext_lazy("Image height")
    )

    ppoi = PPOIField('Image PPOI')

    def toJson(self):
        return {
            'width': self.width,
            'height': self.height,
            'url': self.image.thumb
        }

    def __str__(self):
        return ''

    class Meta:
        verbose_name = gettext_lazy("Gallery Image")
        verbose_name_plural = gettext_lazy("Gallery Images")
        db_table = 'app_projects_project_gallery_image'
        ordering = ['order']