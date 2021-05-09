from django.db import models
from django.utils.translation import gettext_lazy
from imagefield.fields import ImageField, PPOIField
from imagefield.processing import register
from imagefield.processing import register

@register
def force_webp(get_image):
    def processor(image, context):
        image = get_image(image, context)
        context.save_kwargs["format"] = "WebP"
        context.save_kwargs["quality"] = 90
        return image
    return processor

def webp_processor_spec(fieldfile, context):
    context.extension = ".webp"
    context.processors = [
        "force_webp",
    ]

def thumb_webp_processor_spec(fieldfile, context):
    context.extension = ".webp"
    context.processors = [
        ('thumbnail', (250, 180)),
        "force_webp",
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
            'thumb': ['default',  ('thumbnail', (250, 180))],
            'thumb_webp': thumb_webp_processor_spec,
            'full': ['default',],
            'full_webp': webp_processor_spec
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