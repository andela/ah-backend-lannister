import os
import ssl

import sendgrid
from decouple import Csv, config
from sendgrid.helpers.mail import *

ssl._create_default_https_context = ssl._create_unverified_context


def send_gridmail(data, token, url):
    sg = sendgrid.SendGridAPIClient(apikey=config('SENDGRID_API_KEY'))
    from_email = Email("support@ah-haven.com")
    to_email = Email(data)
    subject = 'Password reset Email- AH-Haven'
    content = Content("text/plain", f"You receiving this email because\
                      you need password reset on\
                      Authors haven.\
                      Click the link to reset your password \
                      http://{url}/api/users/password_reset/confirm/{token}/ \
                    DONT share this link with anyone")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return ({'message': f'a reset link has been sent to your email {data}'})
