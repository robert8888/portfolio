from django.db import models
from django_resized import ResizedImageField

class Portal(models.Model):
    name = models.CharField(
            max_length = 100, 
            help_text = "Enter portal name", 
            verbose_name = "Portal name"
        )

    url = models.CharField(
            max_length = 255, 
            help_text = "Enter portal profile url", 
            verbose_name = "Owner profile url"
        )

    logo = ResizedImageField(
            upload_to = "portals", 
            size=[500, 300],
            force_format='PNG',
            help_text = "Portal logo expect 100 x 100 px",
            verbose_name = "Portal logo",
        )

    owner = models.ForeignKey("Owner", on_delete = models.CASCADE)

    def __str__(self):
        return "Portal profile"

    class Meta:
        verbose_name = "Owner Portal"