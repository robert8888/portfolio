from django.contrib import admin
from .models_admin.contact_admin import contactAdmin
from .models import Contact
# Register your models here.

admin.site.register(Contact, contactAdmin)
