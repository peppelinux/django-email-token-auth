import uuid

from django_countries.fields import CountryField
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . utils import (get_default_translations,
                     translate_to,
                     get_default_valid_until)


class Identity(models.Model):
    """
    Provides registry
    """
    personal_title = models.CharField(max_length=12, blank=True, null=True)
    name = models.CharField(max_length=256, blank=False, null=False,
                            help_text=_('Nome o ragione sociale'))
    surname = models.CharField(max_length=135, blank=False, null=False)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=135, blank=True, null=True)
    common_name = models.CharField(max_length=256, blank=True, null=True,
                                   help_text=_('Nome o ragione sociale'))
    country = CountryField(blank=True,
                           help_text=_('nazionalità, cittadinanza'))
    city = models.CharField(max_length=128, blank=True, null=True,
                            help_text=_('residenza'))
    tin = models.CharField(max_length=24, blank=True, null=True,
                           help_text=_(('Taxpayer Identification Number'
                                        ' (codice fiscale)')))
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=128,
                                      blank=True, null=True, help_text='')
    description = models.TextField(max_length=1024, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['created',]
        verbose_name_plural = _("Identità digitali")

    def is_valid(self):
        if not self.expiration_date: return True
        if (timezone.localtime() > self.expiration_date):
            return False
        return True

    def __str__(self):
        return '{} {} - {}'.format(self.name, self.surname, self.email)


class IdentityToken(models.Model):
    identity = models.ForeignKey(Identity, null=True,
                                 on_delete=models.SET_NULL)
    token = models.UUIDField(unique=True, default=uuid.uuid4,
                             blank=True,
                             help_text="/access/$token")
    sent = models.BooleanField(default=False)
    sent_to = models.CharField(max_length=254, blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=False,
                                       default=get_default_valid_until)
    used = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True,
                                    help_text=_('disable it if needed'))
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['create_date',]
        verbose_name_plural = _("Token di accesso")


    def __str__(self):
        return '{} {} - {}'.format(self.identity, self.token, self.used if self.used else '')

    def is_valid(self):
        if (timezone.localtime() > self.valid_until) or \
            not self.is_active or self.used:
            return False
        return True

    def mark_as_sent(self, email):
        self.sent_to = email
        self.sent = True
        self.sent_date = timezone.localtime()
        self.save()

    def mark_as_used(self):
        self.is_active = False
        self.used = timezone.localtime()
        self.save()

    def get_activation_url(self):
        return reverse('email_token_auth:email_token_access',
                       kwargs={'token': self.token })
