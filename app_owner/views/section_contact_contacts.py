from .get_contacts import get as getContacts

def process(request, config, context, *args):
     contacts = getContacts({'on_index': True})
     context['contacts'] = contacts
     return context