from django.contrib import admin

from . models import IdentityToken


@admin.register(IdentityToken)
class IdentityTokenAdmin(admin.ModelAdmin):
    list_display  = ('identity', 'sent', 'used', 'create_date')
    # search_fields = ('identity', 'surname','common_name', 'email', 'telephone')
    list_filter   = ('sent', 'sent_date', 'create_date', 'used')
    readonly_fields = ('token', 'create_date', #'used',
                       'sent_date', 'sent', 'identity')
    fieldsets = (
                    (None, { 'fields' :
                               (('identity', 'is_active'),
                                ('token', ),
                                ('sent', 'sent_to', 'sent_date', ),
                                ('valid_until', ),
                                ('used', 'ldap_dn'),
                                ('create_date',),
                                )
                           }
                    ),
                )

    #actions = [send_email_renew_password,]
    date_hierarchy = 'create_date'

    # class Media:
        # js = ('js/textarea-autosize.js',)
