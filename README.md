# django-email-token-auth
Django app to authenticate users with tokens sent by email.

Django-email-token-auth is not a pure Authentication Backend, it
login users defined in a separate schema if their profiles are valid (not expired).

When a user get a token through email and use it to gain access, an
user without a password will be created in the user model.

Workflow described as follow:

 - A guy requests an access submitting his email in a webform;
 - If this email is found in the Identity Model a token will be created;
 - The token is sent to the guy's email;
 - The user click on the token url found in the email and get redirected to a web form;
 - The user submit again his email to confirm the access validity, and if the token is not expired and the email matchess with the token...

The user gets logged in as a normal Django user.

settings.py
-----------
Parameters to be configured.
See `example/example/settings.py` for a complete example configuration.

````
TOKEN_EMAIL_MSG = _("""Dear {user},

This message was sent to you by https://{hostname}, your IDentity Manager.
Please do not reply to this email.

Click on this resource to gain access: https://{hostname}{url}
This resource will be available for {minutes} minutes before expiring.

If you're experiencing in problems please contact our technical staff.
Best regards""")

TOKEN_EXPIRATION_MINUTES = 5
MSG_DEFAULT_LANGUAGES = ['it', 'en']
````

License
-------

BSD
