from django.contrib import admin

from interest.models import Interest


class InterestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Interest, InterestAdmin)
