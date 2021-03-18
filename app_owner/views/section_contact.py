from app_owner.models import Contact, ContactImage
from django.db import connection
from portfolio.utils.memoize import memoize
from portfolio.s3proxy import generatePresignedUrl
from django.conf import settings

# def process(request, config, context, *args):
#     contacts = Contact.objects.select_related('contactimage').all()
#     contact_images_ids = [contact.contactimage.id for contact in contacts]
#
#     contact_images = {}
#     for contact_image in ContactImage.objects.filter(id__in = contact_images_ids):
#         contact_images[contact_image.contact.id] = contact_image
#
#     contacts_data = []
#     for contact in Contact.objects.select_related('contactimage').all():
#         contact = {
#             'name' : contact.name,
#             **({'url': contact.url } if not contact.is_number() else {}),
#             **({'number': contact.number } if contact.is_number() else {}),
#             'contact_image': contact_images[contact.id],
#             'is_number': contact.is_number()
#         }
#         contacts_data.append(contact)
#
#     context['contacts'] = contacts_data
#     print("----", context['contacts'][0].get('contact_image').image.source.url)
#     return context

# because djnago ORM is slow - direct database lookup speed up loading context data
def process(request, config, context, *args):
    query = f"""
    SELECT
    app_owner_contact.name,
    app_owner_contactportal.url,
    app_owner_contactnumber.number,
    app_owner_image.source,
    app_owner_image.width,
    app_owner_image.height,
    app_owner_contactimagesprite.width,
    app_owner_contactimagesprite.height,
    app_owner_contactimagesprite.top,
    app_owner_contactimagesprite.left
    FROM app_owner_contact
    LEFT JOIN app_owner_contactportal ON app_owner_contact.id = app_owner_contactportal.contact_ptr_id
    LEFT JOIN app_owner_contactnumber ON app_owner_contact.id = app_owner_contactnumber.contact_ptr_id
    LEFT JOIN app_owner_contactimage ON app_owner_contact.id = app_owner_contactimage.contact_id
    LEFT JOIN app_owner_image ON app_owner_image.id = app_owner_contactimage.image_id
    LEFT JOIN app_owner_contactimagestandalone ON app_owner_contactimagestandalone.contactimage_ptr_id = app_owner_contactimage.id
    LEFT JOIN app_owner_contactimagesprite ON app_owner_contactimagesprite.contactimage_ptr_id = app_owner_contactimage.id
    ORDER BY app_owner_contact.order
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    getImgUrl = memoize(generatePresignedUrl)
    context['contacts'] = [{
            'name' : row[0],
            'is_number': True if row[2] else False,
            **({'url': row[1] } if not row[1] else {}),
            **({'number': row[2] } if row[2] else {}),
            "img_url": getImgUrl(settings.MEDIA_ROOT_PATH + row[3]),
            "img_is_sprite": True if not None in row[6:] else False,
            "img_width": row[4] if None in row[6:] else row[6],
            "img_height": row[5] if None in row[6:] else row[7],
            **({'img_top': row[8] } if not row[8] == None else {}),
            **({'img_left': row[9] } if not row[9] == None else {}),
        } for row in rows ]
    return context