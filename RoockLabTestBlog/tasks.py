from __future__ import absolute_import, unicode_literals
from RoockLabTestBlog.celery import app
from django.core.mail import send_mail


@app.task
def send_email(recipient_list, subject, body, from_address):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    send_mail(
        subject,
        body,
        from_address,
        list(recipient_list)
    )
