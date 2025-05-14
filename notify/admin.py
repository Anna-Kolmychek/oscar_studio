from django.contrib import admin

from notify.models import RecipientTG, RecipientEmail, Notification, \
    NotificationLog


class RecipientTGInline(admin.TabularInline):
    model = RecipientTG
    fields = ('recipient', )
    extra = 0


class RecipientEmailInline(admin.TabularInline):
    model = RecipientEmail
    fields = ('recipient', )
    extra = 0


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'delay', 'created_at', )
    list_display_links = ('message', )

    fields = ('message', 'delay', 'created_at', )
    inlines = (RecipientTGInline, RecipientEmailInline, )

    readonly_fields = ('created_at', )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('notification', 'recipient', 'created_at', 'status')
    list_display_links = ('notification',)

    fields = ('notification', 'recipient', 'created_at', 'status',
              'error_message',)

    readonly_fields = ('created_at', 'recipient', )
