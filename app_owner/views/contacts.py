from portfolio.utils.execute_db_queries import execute_queries
from sqlescapy import sqlescape
from portfolio.s3proxy import generatePresignedUrl
from django.conf import settings

def buildQuery(params):
    def typeCondition():
        if not params.get("type"): return ""
        value = sqlescape(params.get("type"), '')
        return 'contact.type = ' + value

    def onIndexCondition():
        if not params.get("on_index"): return ""
        value = params.get("on_index")
        value = "TRUE" if value else "FALSE"
        return 'contact.on_index = ' + value

    def where():
        conditions = [
            condition
            for condition in [typeCondition(), onIndexCondition()]
            if condition != ""
        ]
        if not len(conditions): return ""
        return 'WHERE ' + ' AND '.join(conditions)

    return f"""
    SELECT * FROM
    (SELECT
    app_owner_contact.name as "name",
    (CASE WHEN app_owner_contactnumber.number IS NOT NULL THEN TRUE ELSE FALSE END) as "is_number",
    (CASE
      WHEN app_owner_contactnumber.number IS NOT NULL THEN 'number'
      WHEN app_owner_contactaddress.address IS NOT NULL THEN 'address'
      WHEN app_owner_contactportal.url IS NOT NULL THEN 'portal'
      ELSE ''
    END) as "type",
    (CASE
      WHEN app_owner_contactnumber.number IS NOT NULL THEN app_owner_contactnumber.number
      WHEN app_owner_contactaddress.address IS NOT NULL THEN app_owner_contactaddress.address
      WHEN app_owner_contactportal.url IS NOT NULL THEN app_owner_contactportal.url
      ELSE ''
    END) as "value",
    app_owner_image.source as "img_path",
    (CASE WHEN app_owner_contactimagesprite.width IS NOT NULL THEN TRUE ELSE FALSE END) as "img_sprite",
    (CASE
      WHEN app_owner_contactimagesprite.width IS NOT NULL
      THEN app_owner_contactimagesprite.width
      ELSE app_owner_image.width
    END) as "img_width",
    (CASE
      WHEN app_owner_contactimagesprite.height IS NOT NULL
      THEN app_owner_contactimagesprite.height
      ELSE app_owner_image.height
    END) as "img_height",
    app_owner_contactimagesprite.top as "img_top",
    app_owner_contactimagesprite.left as "img_left",
    app_owner_contact.show_on_index as "on_index"
    FROM app_owner_contact
    LEFT JOIN app_owner_contactportal ON app_owner_contact.id = app_owner_contactportal.contact_ptr_id
    LEFT JOIN app_owner_contactnumber ON app_owner_contact.id = app_owner_contactnumber.contact_ptr_id
    LEFT JOIN app_owner_contactaddress ON app_owner_contact.id = app_owner_contactaddress.contact_ptr_id
    LEFT JOIN app_owner_contactimage ON app_owner_contact.id = app_owner_contactimage.contact_id
    LEFT JOIN app_owner_image ON app_owner_image.id = app_owner_contactimage.image_id
    LEFT JOIN app_owner_contactimagestandalone ON app_owner_contactimagestandalone.contactimage_ptr_id = app_owner_contactimage.id
    LEFT JOIN app_owner_contactimagesprite ON app_owner_contactimagesprite.contactimage_ptr_id = app_owner_contactimage.id
    ORDER BY app_owner_contact.order) as contact
    {where()}
    """

def get(prams):
    query = buildQuery(prams)
    query_results = execute_queries([query])
    if not query_results['successAll']: return {}
    contacts = query_results['resultEach'][0]['data']
    for contact in contacts:
        img_path = contact.get("img_path", None)
        if img_path:
            contact["img_url"] = generatePresignedUrl(settings.MEDIA_ROOT_PATH + img_path)

    return contacts