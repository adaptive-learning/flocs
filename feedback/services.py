"""
Feedback services
"""

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

MIN_TEXT_LENGTH = 4

EMAIL_BODY_TEMPLATE = """
text:
{text}

email:
{email}

user_id:
{user_id}
"""


def process_feedback_message(text, email, user_id):
    email_body = EMAIL_BODY_TEMPLATE.format(
        text=text,
        email=email if email else '[missing]',
        user_id=user_id
    )

    logger.info("New feedback: " + email_body)
    if len(text) >= MIN_TEXT_LENGTH:
        _mail_feedback_to_admins(email_body)


def _mail_feedback_to_admins(text):
    try:
        send_mail('[flocs] Feedback Message', text, 'feedback-form@flocs.thran.cz',
            settings.EMAIL_ADMINS)
    except Exception as exc:
        logger.error('Sending mail failed: ' + str(exc))
        raise
