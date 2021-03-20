from django.db import models
from django.utils.translation import gettext_lazy
from polymorphic.models import PolymorphicModel


class ContactImage(PolymorphicModel):
    IS_SPRITE = False

    contact = models.OneToOneField(
        'Contact',
        on_delete=models.CASCADE,
    )

    image = models.ForeignKey(
        'Image',
        on_delete=models.CASCADE,
    )

    def is_sprite(self):
        return self.IS_SPRITE


    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = gettext_lazy("Contact image")


class ContactImageStandalone(ContactImage):
    class Meta:
        verbose_name = gettext_lazy("Image")


class ContactImageSprite(ContactImage):
    IS_SPRITE = True

    top = models.DecimalField(
        verbose_name = gettext_lazy("Top"),
        max_digits=10,
        decimal_places=2
    )

    left = models.DecimalField(
        verbose_name = gettext_lazy("Left"),
        max_digits=10,
        decimal_places=2
    )

    width = models.DecimalField(
        verbose_name = gettext_lazy("Width"),
        max_digits=10,
        decimal_places=2
    )

    height = models.DecimalField(
        verbose_name = gettext_lazy("Height"),
        max_digits=10,
        decimal_places=2
    )


    class Meta:
        verbose_name = gettext_lazy("Sprite image")



class Image(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy("Image identification name")
    )

    source = models.ImageField(
        upload_to = 'portals',
        width_field = 'width',
        height_field = 'height'
    )

    width = models.PositiveIntegerField()

    height = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Image")