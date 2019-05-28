from django.conf import settings
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from . forms import EmailForm
from . models import *


def email_token_access(request, token):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(''))
    elif request.method == 'GET':
        form = EmailForm()
    elif request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            idtoken = IdentityToken.objects.filter(identity__email=email,
                                                   identity__is_active=True,
                                                   token=token,
                                                   is_active=True)
            if idtoken.is_valid():
                udict = dict(username=idtoken.identity.username,
                             first_name=idtoken.identity.name,
                             last_name=idtoken.identity.surname,
                             email=idtoken.identity.email,
                             is_active=True)
                # return HttpResponse('not valid')
                user = User.objects.filter(**udict).first()
                if not user:
                    User.objects.create(**udict)
                    login(request, user)
                return HttpResponseRedirect(reverse(''))

    return render(request, 'email_token_access.html',
                  context={'form': form})
