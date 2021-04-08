from django.db import models
from django import forms
from django.forms.widgets import Input
import colorsys

import re

class ColorConverter:
    @staticmethod
    def rgb_to_hsl(r,g,b,a = None):
        if not (0 <= r <=255): raise ValueError("r (red) parameter must be between 0 and 255.")
        if not (0 <= g <=255): raise ValueError("g (green) parameter must be between 0 and 255.")
        if not (0 <= b <=255): raise ValueError("b (blue) parameter must be between 0 and 255.")

        var_R = r/255.0
        var_G = g/255.0
        var_B = b/255.0
        h, l, s = colorsys.rgb_to_hls(var_R, var_G, var_B)
        return h, s, l
            # From http://sebsauvage.net/python/snyppets/#hsl
#         if not (0 <= r <=255): raise ValueError("r (red) parameter must be between 0 and 255.")
#         if not (0 <= g <=255): raise ValueError("g (green) parameter must be between 0 and 255.")
#         if not (0 <= b <=255): raise ValueError("b (blue) parameter must be between 0 and 255.")
#
#         var_R = r/255.0
#         var_G = g/255.0
#         var_B = b/255.0
#
#         var_Min = min( var_R, var_G, var_B )    # Min. value of RGB
#         var_Max = max( var_R, var_G, var_B )    # Max. value of RGB
#         del_Max = var_Max - var_Min             # Delta RGB value
#
#         l = ( var_Max + var_Min ) / 2.0
#         h = 0.0
#         s = 0.0
#         if del_Max!=0.0:
#             if l<0.5: s = del_Max / ( var_Max + var_Min )
#             else:     s = del_Max / ( 2.0 - var_Max - var_Min )
#             del_R = ( ( ( var_Max - var_R ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
#             del_G = ( ( ( var_Max - var_G ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
#             del_B = ( ( ( var_Max - var_B ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
#             if    var_R == var_Max : h = del_B - del_G
#             elif  var_G == var_Max : h = ( 1.0 / 3.0 ) + del_R - del_B
#             elif  var_B == var_Max : h = ( 2.0 / 3.0 ) + del_G - del_R
#             while h < 0.0: h += 1.0
#             while h > 1.0: h -= 1.0
#
#         if a:
#             return (h,s,l,a)
#         else:
#             return (h,s,l)

    @staticmethod
    def hex_to_rgb(hex):
        hex_re = re.compile('\#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$')
        hex_match = hex_re.match(hex)
        if not hex_match:
            return (0, 0, 0)

        if hex.startswith('#'):
            hex = hex[1:]

        if len(hex) == 6:
            r,g,b = tuple(int(hex[i:i+2], 16) for i in range(0, 6, 2))
        else:
            r,g,b = tuple(int(hex[i:i+1], 16)*17 for i in range(0, 3))

        return (r, g, b)


    @staticmethod
    def hex_to_hsl(hex):
        r, g, b = ColorConverter.hex_to_rgb(hex)
        h, s, l = ColorConverter.rgb_to_hsl(r, g, b)
        return (h, s, l)


class Color:
    def __init__(self, hex):
        self.hex = hex

    @property
    def hsl(self):
        return ColorConverter.hex_to_hsl(self.hex)

    @property
    def hsl_dict(self):
        h, s, l = ColorConverter.hex_to_hsl(self.hex)
        return { 'h': str(h * 360), 's': str(s * 100) + '%', 'l': str(l * 100) + '%' }

    @property
    def rgb(self):
        return ColorConverter.hex_to_rgb(self.hex)

    def __str__(self):
        return self.hex

class ColorInput(Input):
    input_type = 'color'
    template_name = 'django/forms/widgets/text.html'

class ColorFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = ColorInput
        super().__init__(*args, **kwargs)

class ColorField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': ColorFormField
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def from_db_value(self, value, expression, connection):
        return Color(value)

    def to_python(self, value):
        if isinstance(value, Color):
            return value
        if value is None:
            return value
        hex = super().to_python(value)
        return Color(hex)

    def get_prep_value(self, value):
        if isinstance(value, Color):
            value = value.hex
        return super().get_prep_value(value)

    def get_db_prep_save(self, value, connection):
        if isinstance(value, Color):
            return super().get_db_prep_save(value.hex, connection)
        elif isinstance(value, str):
            return super().get_db_prep_save(value, connection)

    def db_type(self, connection):
        return 'varchar'