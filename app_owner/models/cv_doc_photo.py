from django.db import models
from django.utils.translation import gettext_lazy
from imagefield.fields import ImageField, PPOIField


class CVDocumentPhoto(models.Model):
    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy("Photo identification name")
    )

    source = ImageField(
        verbose_name = gettext_lazy("Image"),
        height_field = 'height',
        width_field = 'width',
        ppoi_field = 'ppoi',
        upload_to = 'cv-photo/',
        formats = {
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


    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy("Photo")
        verbose_name_plural = gettext_lazy("Photos")
        db_table = 'app_owner_cv_doc_photo'