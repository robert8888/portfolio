from django.db import models

VIEWS = [
    ('projects', 'Projects'),
    ('stack', 'Stack'),
    ('contact', 'Contact'),
]

class View(models.Model):
    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        max_length = 255,
        choices = VIEWS,
        default = '',
        null = True,
    )