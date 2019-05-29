from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . models import IdentityToken, Identity


class IdentityTokenForm(forms.ModelForm):
    class Meta:
        model = IdentityToken
        fields = ('__all__')

    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(IdentityTokenForm, self).has_changed(*args, **kwargs)


class IdentityTokenInline(admin.StackedInline):
    form  = IdentityTokenForm
    model = IdentityToken
    readonly_fields = ('create_date', 'sent_date',
                       'sent', 'identity', 'used')
    fieldsets = (
                    (None, { 'fields' :
                               (('token', 'is_active'),
                                ('sent', 'sent_date'),
                                ('valid_until',),
                                ('create_date','used',))
                           }
                    ),
                )
    extra = 0


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    inlines = [IdentityTokenInline,]
    list_display  = ('name', 'surname','email', 'created')
    search_fields = ('name', 'surname','common_name',
                     'email', 'telephone')
    list_filter   = ('created',)
    readonly_fields = ('created', 'modified')
    fieldsets = (
                (None, { 'fields' :
                    (
                       ('name', 'surname'),
                       ('email', 'telephone', ),
                       ('created', 'modified'),
                       ('expiration_date')
                    )}),
                (_('Extended Attributes'), {
                        'classes': ('collapse',),
                        'fields' :
                        (
                            ('personal_title', 'common_name'),
                            ('country', 'city', ),
                            ('tin',),
                            ('place_of_birth', 'date_of_birth'),
                            # ('document_front', 'document_retro',),
                            ('description',),
                        )}
                    ),
                )

    #autocomplete_fields = ['country',]
    #actions = [send_email_renew_password,]
    date_hierarchy = 'created'

    class Media:
        js = ('js/textarea-autosize.js',)


@admin.register(IdentityToken)
class IdentityTokenAdmin(admin.ModelAdmin):
    list_display  = ('identity', 'sent', 'used', 'create_date')
    # search_fields = ('identity', 'surname','common_name', 'email', 'telephone')
    list_filter   = ('sent', 'sent_date', 'create_date', 'used')
    readonly_fields = ('token', 'create_date', #'used',
                       'sent_date', 'sent', 'sent_to')
    fieldsets = (
                    (None, { 'fields' :
                               (('identity', 'is_active'),
                                ('token', ),
                                ('sent', 'sent_to', 'sent_date', ),
                                ('valid_until', ),
                                ('create_date', 'used'),
                                )
                           }
                    ),
                )

    #actions = [send_email_renew_password,]
    date_hierarchy = 'create_date'

    # class Media:
        # js = ('js/textarea-autosize.js',)
