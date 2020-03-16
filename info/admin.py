from django.contrib import admin
from .models import Tip
# Register your models here.


class TipAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Tip, TipAdmin)
