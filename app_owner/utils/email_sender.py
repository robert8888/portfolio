import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send(req, context, template_names):
    BASE_DIR = settings.BASE_DIR
    sender_email = os.getenv('EMAIL_HOST_USER')
    target_email = os.getenv('SYSTEM_EMAIL_TARGET')

    subject = context['subject']

    html_version = os.path.join(BASE_DIR, 'app_cms_tpl/templates/emails/' + template_names['html'])
    plain_version = os.path.join(BASE_DIR, 'app_cms_tpl/templates/emails/' + template_names['plain'])
    html_message = render_to_string(html_version, context = context)
    plain_message = render_to_string(plain_version, context = context)

    message = EmailMultiAlternatives(subject, plain_message, sender_email, [target_email])
    message.attach_alternative(html_message, "text/html")
    message.send()