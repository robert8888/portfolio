from django.db import models
from django.utils.translation import gettext_lazy
from portfolio.db.color_field import ColorField


class CVColorProfile(models.Model):
    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Color profile identification name')
    )

    background = ColorField(
        verbose_name = gettext_lazy('Primary background color'),
        default = '#FFFFFF'
    )

    primary = ColorField(
        verbose_name = gettext_lazy('Primary color'),
        default = '#aa3339'
    )

    secondary = ColorField(
        verbose_name = gettext_lazy('Secondary color'),
        default = '#f7f1e1'
    )

    text_primary = ColorField(
        verbose_name = gettext_lazy('Primary text color'),
        default = '#f7f1e1'
    )

    text_primary_focus = ColorField(
        verbose_name = gettext_lazy('Primary text color - focus'),
        default = '#f7f1e1'
    )

    text_secondary = ColorField(
        verbose_name = gettext_lazy('Secondary text color'),
        default = '#f7f1e1'
    )

    text_secondary_focus = ColorField(
        verbose_name = gettext_lazy('Secondary text color - focus'),
        default = '#f7f1e1'
    )


    def __str__(self):
        return self.id_name

    class Meta:
        db_table = 'app_owner_cv_color_profile'
