from django.db import models
from solo.models import SingletonModel

class Owner(SingletonModel):
    name = models.CharField(
            max_length = 255,
            default = '',
            verbose_name  = 'Name'
        )

    surname = models.CharField(
            max_length = 255,
            default = '',
            verbose_name = 'Surname'
        )

    birthdate = models.DateField(
            auto_now=False,
            auto_now_add=False,
            verbose_name = "Birthdate",
            blank = True,
            null = True
        )

    about_short = models.TextField(
            default = '',
            verbose_name = "Short description"
        )

    about_full = models.TextField(
            default = '',
            verbose_name = 'Full description'
        )

    photo = models.ImageField(
            upload_to = 'author',
            height_field = 'photo_height',
            width_field = 'photo_width',
            max_length = 255,
            verbose_name = 'Photo',
            help_text = 'Select author photo'
        )

    photo_width = models.PositiveIntegerField(default = 0)

    photo_height = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return "Owner"

    class Meta:
        verbose_name = "Owner"