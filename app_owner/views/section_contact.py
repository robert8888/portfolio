from app_owner.models import Contact, ContactImage
from django.db import connection
from portfolio.utils.memoize import memoize
from portfolio.s3proxy import generatePresignedUrl
from django.conf import settings
from .contacts import get as getContacts

def process(request, config, context, *args):
     contacts = getContacts({'on_index': True})
     context['contacts'] = contacts
     return context