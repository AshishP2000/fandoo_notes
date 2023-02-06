from celery import shared_task
from django.core.mail import send_mail
from rest_framework.reverse import reverse

from fundoo_notes import settings
from user.utils import JWT


@shared_task
def add_func(token, data):
    send_mail(
        'fundoo notes',
        settings.BASE_URL + reverse('verify', kwargs={'token': token}),
        settings.EMAIL_HOST_USER,
        [data.get('email')]
    )
