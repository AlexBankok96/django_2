from django.core.cache import cache

from .models import  Mailing, MailingAttempt, Client
from users.models import User

def get_index_page_cache_data(user: User) -> dict:
    """Функция возвращает кешированные данные для главной страницы"""

    # проверяем кеш, если есть - отдаем в контроллер
    context_from_cache = cache.get(f"index_page_data/{user.email}")
    if context_from_cache:
        return context_from_cache


    context_update = {}
    if user.groups.filter(name="Менеджер").exists():
        mailing_attempt = MailingAttempt.objects.all()
        mailing = Mailing.objects.all()
        recipient = Client.objects.all()

    else:
        mailing_attempt = MailingAttempt.objects.filter(mailing__owner=user.id)
        mailing = Mailing.objects.filter(owner=user.id)
        recipient = Client.objects.filter(owner=user.id)

    attempt_count = mailing_attempt.count()
    attempt_success_count = mailing_attempt.filter(status="success").count()
    attempt_failure_count = mailing_attempt.filter(status="failure").count()
    mailing_count = mailing.count()
    mailing_running_count = mailing.filter(status="running").count()
    recipient_count = recipient.count()
    context_update["object_list"] = mailing_attempt
    context_update["attempt_count"] = attempt_count
    context_update["attempt_success_count"] = attempt_success_count
    context_update["attempt_failure_count"] = attempt_failure_count
    context_update["mailing_count"] = mailing_count
    context_update["mailing_running_count"] = mailing_running_count
    context_update["recipient_count"] = recipient_count
    cache.set(f"index_page_data/{user.email}", context_update, 5)
    return context_update

