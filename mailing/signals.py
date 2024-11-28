from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from users.models import User
from mailing.models import Mailing, Message


@receiver(post_save, sender=User)
def dump_user_data(sender, instance, created, **kwargs):
    if created:
        call_command('dumpdata', 'users.user', output='users_fixture.json', indent=4)


@receiver(post_save, sender=Message)
def dump_message_data(sender, instance, created, **kwargs):
    if created:
        call_command('dumpdata', 'mailing.message', output='message_fixture.json', indent=4)


@receiver(post_save, sender=Mailing)
def dump_mailing_data(sender, instance, created, **kwargs):
    if created:
        call_command('dumpdata', 'mailing.mailing', output='mailing_fixture.json', indent=4)
