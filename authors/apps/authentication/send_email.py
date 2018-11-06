import os
import ssl

import sendgrid
from decouple import Csv, config
from sendgrid.helpers.mail import *
from django.template.loader import render_to_string

ssl._create_default_https_context = ssl._create_unverified_context


def send_gridmail(data,url):
    message_template = "password_reset.html"
    message = render_to_string(message_template,{"url":url})
    sg = sendgrid.SendGridAPIClient(apikey=config('SENDGRID_API_KEY'))
    from_email = Email("support@ah-haven.com")
    to_email = Email(data)
    subject = 'Password reset Email- AH-Haven'
    content = Content("text/html",message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return ({'message': f'a reset link has been sent to your email {data}'})
