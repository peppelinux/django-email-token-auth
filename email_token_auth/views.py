from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from . decorators import *
from . forms import EmailForm
from . models import *


def _handle_request(request):
    if request.method == 'GET':
        return EmailForm()
    elif request.method == 'POST':
        return EmailForm(request.POST)


@redirect_if_authenticated(settings.LOGIN_REDIRECT_URL)
def email_token_request(request):
    form = _handle_request(request)
    if form.is_valid():
        email = form.cleaned_data['mail']
        # check if the identity is valid
        identity = Identity.objects.filter(email=email).last()
        if not identity or not identity.is_valid():
            return render(request, 'email_token_sent.html',
                          context={'form': form})

        # create a valid token
        idtoken = IdentityToken.objects.filter(is_active=True,
                                               identity__email = email).last()
        if not idtoken or not idtoken.is_valid():
            idtoken = IdentityToken.objects.create(identity=identity)

        d = {'url': idtoken.get_activation_url(),
             'user': identity.name,
             'hostname': settings.HOSTNAME,
             'minutes': settings.TOKEN_EXPIRATION_MINUTES}
        # IDENTITY_PROVISIONING_MSG - two language for everyone!
        mail_subject = get_default_translations(_('{} - New access request').format(settings.HOSTNAME),
                                                sep = ' - ')

        body_translated = []
        for lang in settings.MSG_DEFAULT_LANGUAGES:
            t = translate_to(settings.TOKEN_EMAIL_MSG, lang)
            if t not in body_translated:
                body_translated.append(t)

        sent = send_mail(mail_subject,
                         ''.join(body_translated).format(**d),
                         settings.DEFAULT_FROM_EMAIL,
                         [email,],
                         fail_silently=True,
                         auth_user=None,
                         auth_password=None,
                         connection=None,
                         html_message=None)
        if sent:
            idtoken.mark_as_sent(email)

        return render(request, 'email_token_sent.html',
                  context={'form': form})

    return render(request, 'email_token_access.html',
                  context={'form': form})


@redirect_if_authenticated('home')
def email_token_access(request, token):
    form = _handle_request(request)
    if form.is_valid():
        email = form.cleaned_data['mail']
        idtoken = IdentityToken.objects.filter(identity__email=email,
                                               token=token,
                                               is_active=True).last()
        if idtoken.is_valid():
            udict = dict(username=idtoken.identity.email,
                         first_name=idtoken.identity.name,
                         last_name=idtoken.identity.surname,
                         email=idtoken.identity.email,
                         is_active=True)
            # return HttpResponse('not valid')
            User = get_user_model()
            user = User.objects.filter(**udict).first()
            if not user:
                User.objects.create(**udict)

            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        if not idtoken or not idtoken.is_valid():
            return render(request, 'email_token_notvalid.html')

    return render(request, 'email_token_access.html',
                  context={'form': form})
