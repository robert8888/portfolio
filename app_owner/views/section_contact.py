from app_owner.models import Contact, ContactImage

def process(request, config, context, *args):
    contacts = Contact.objects.select_related('contactimage').all()
    contact_images_ids = [contact.contactimage.id for contact in contacts]

    contact_images = {}
    for contact_image in ContactImage.objects.filter(id__in = contact_images_ids):
        contact_images[contact_image.contact.id] = contact_image

    contacts_data = []
    for contact in Contact.objects.select_related('contactimage').all():
        contact = {
            'name' : contact.name,
            **({'url': contact.url } if not contact.is_number() else {}),
            **({'number': contact.number } if contact.is_number() else {}),
            'contact_image': contact_images[contact.id],
            'is_number': contact.is_number()
        }
        contacts_data.append(contact)

    print(contacts_data[0]["contact_image"].width)
    context['contacts'] = contacts_data
    return context