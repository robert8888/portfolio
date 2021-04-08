from django.db import models
from django.utils.translation import gettext_lazy
from portfolio.db.color_field import ColorField


class CVColorProfile(models.Model):
    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Color profile identification name')
    )

    background = ColorField(
        verbose_name = gettext_lazy('Background color'),
        default = '#FFFFFF'
    )

    text = ColorField(
        verbose_name = gettext_lazy('Text color'),
        default = '#FFFFFF'
    )

    text_focus = ColorField(
        verbose_name = gettext_lazy('Text focus color')
    )

    primary = ColorField(
        verbose_name = gettext_lazy('Primary color'),
        default = '#aa3339'
    )

    text_primary_focus = ColorField(
        verbose_name = gettext_lazy('Primary text color - focus'),
        default = '#f7f1e1'
    )

    text_secondary = ColorField(
        verbose_name = gettext_lazy('Secondary text color'),
        default = '#f7f1e1'
    )

    secondary = ColorField(
        verbose_name = gettext_lazy('Secondary color'),
        default = '#f7f1e1'
    )

    text_primary = ColorField(
        verbose_name = gettext_lazy('Primary text color'),
        default = '#f7f1e1'
    )

    text_secondary_focus = ColorField(
        verbose_name = gettext_lazy('Secondary text color - focus'),
        default = '#f7f1e1'
    )

    @property
    def colors(self):
        return {
            'background': self.background,
            'text': self.text,
            'text-focus': self.text_focus,

            'primary': self.primary,
            'text-primary': self.text_primary,
            'text-primary-focus': self.text_primary_focus,

            'secondary': self.secondary,
            'text-secondary':self.text_secondary,
            'text-secondary-focus':self.text_secondary_focus
        }

    def __str__(self):
        return self.id_name

    class Meta:
        db_table = 'app_owner_cv_color_profile'
