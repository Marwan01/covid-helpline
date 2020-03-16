from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Subscriber, SubscriberAdmin)
