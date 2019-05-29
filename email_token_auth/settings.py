from django.utils.translation import ugettext_lazy as _

TOKEN_EMAIL_MSG = _("""Dear {user},

This message was sent to you by https://{hostname}, your IDentity Manager.
Please do not reply to this email.

Click on this resource to gain access: https://{hostname}{url}
This resource will be available for {minutes} minutes before expiring.

If you're experiencing in problems please contact our technical staff.
Best regards""")

TOKEN_EXPIRATION_MINUTES = 5
MSG_DEFAULT_LANGUAGES = ['it', 'en']
