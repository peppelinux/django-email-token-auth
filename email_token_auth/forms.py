from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class EmailForm(forms.Form):
    mail = forms.EmailField(label="", max_length=64,
                            help_text=_("name.surname@email.eu "
                                        "or other email used for registration"
                                        ". "),
                            widget=forms.EmailInput(attrs={'class': '',
                                                           'placeholder': _('email@domain.eu')+' ...'}))
