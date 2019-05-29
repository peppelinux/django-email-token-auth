# django-email-token-auth
Django app to authenticate a user using a token sent by email.

Django-email-token-auth is not a pure Authentication Backend but it can
login users defined in a separate schema, if their profiles are valid (not expired).

Once a user get a token through it's mailbox and use this to gain access, a
user without a password will be create in django's user model.

Workflow described as follow:

 - A guy requests an access submitting his email;
 - If this email is found in the Identity Model a token will be created;
 - The token is sent by server to the guy to his email box;
 - the user click on the token url found in the email and get redirected to a web form;
 - He submit again his email, to confirmation, and if the token is not expired...

The user is now logged in.

settings.py
-----------
Parameters to be configured.
See `example/example/settings.py` for an example configuration.

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
