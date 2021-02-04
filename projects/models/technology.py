from django.db import models
from solo.models import SingletonModel

class Technology(SingletonModel):
    name = models.CharField(
            max_length=255, 
            default='Name', 
            help_text='Enter technology name'
        )

    description = models.CharField(
            max_length=255, 
            default="Description", 
            help_text='Enter technology description', 
            blank = True, 
            null = True
        )

    is_main = models.BooleanField(
            verbose_name = "Is owner main technology ?"
        )

    rate = models.DecimalField(
            verbose_name = "Skill rete", 
            max_digits= 2, 
            decimal_places=1, 
            blank = True, 
            null = True
        )

    logo = models.ImageField(
            upload_to='technology', 
            height_field='logo_width',
            width_field='logo_height',
            max_length=255
        )

    logo_width = models.PositiveIntegerField(default = 0)

    logo_height = models.PositiveIntegerField(default = 0)

    weight = models.PositiveIntegerField(
            verbose_name ="Order weight", 
            default = 0
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Technologie"