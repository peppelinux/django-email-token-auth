from django.urls import include, path, re_path
from .views import *

app_name = "email_token_auth"

urlpatterns = [

    path(
        'access/request',
        email_token_request,
        name='email_token_request',
    ),

    path(
        'access/<uuid:token>',
        email_token_access,
        name='email_token_access',
    ),
]
