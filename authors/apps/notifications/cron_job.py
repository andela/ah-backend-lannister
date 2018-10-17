from django_cron import CronJobBase, Schedule
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import Notification, CommentNotification


class EmailNotificationCron(CronJobBase):
    """Create the cron job for email sending."""

    RUN_EVERY_MINS = settings.RUN_EVERY_MINS
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'authors.apps.notifications.cron_job.EmailNotificationCron'

    def do(self):
        """Send emails to all the persons to be notified."""
        subject = 'Authors Haven Notification'

        article_recipients = []
        notifications = Notification.objects.all()
        message_template = "article_notification.html"
        self.send_notification(
            notifications, article_recipients, message_template, subject)

        comment_recipients = []
        notifications = CommentNotification.objects.all()
        message_template = "comment_notification.html"
        self.send_notification(
            notifications, comment_recipients, message_template, subject)

    def send_notification(self, notifications, recipients, message_template, subject):
        for notification in notifications:
            if not notification.email_sent:
                self.get_recipients(notification, recipients)
                content = {'notification': notification}
                message = render_to_string(message_template, content)
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    to=recipients,
                    from_email=settings.EMAIL_HOST_USER)
                mail.content_subtype = "html"
                mail.send(fail_silently=False)
                notification.email_sent = True
                notification.save()

    def get_recipients(self, notification, recipients):
        for user in notification.notified.all():
            if (user not in notification.read.all()
                    and user.profile.email_notification_enabled):
                recipients.append(user.email)
