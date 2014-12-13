import logging

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(user_login_failed)
def log_failed_login(sender, **kwargs):
    logger.info("login attempt for username '{}' failed".format(
        kwargs['credentials']['username'])
    )
