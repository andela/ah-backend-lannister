import datetime
import math
import re

from django.core.mail import EmailMessage
from django.utils.text import slugify


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__
 
    while ModelClass._default_manager.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, extension)
        extension += 1
 
    return unique_slug

def time(string, image=0):
        """
        calculate the read time 
        """
        count = len(re.findall(r'\w+', string))
        read_speed = 200
        time_sec = math.ceil(count/read_speed*60)
        readtime = int(time_sec)
        image_time = 10
        for image in range(image):
            readtime += image_time
        return str(datetime.timedelta(seconds=readtime))

def shareArticleMail(share, request, share_data, article):
        user_instance = request.user
        host = "https://ah-frontend-lannister.herokuapp.com"
        user = user_instance.username
        subject = article.title
        share_slug = article.slug
        body = 'Click on the link below to view Article! \n\n \
                {}/view-article/{} \n\n shared by [ {} ]'.format(
                    host, share_slug, user)
        to_email = [share['email']]
        email = EmailMessage(subject, body, to=to_email,)
        email.send()
        share_data.update({
            'message': 'Article shared succesfully'
                    })
