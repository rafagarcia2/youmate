from django.contrib import admin

from reference.models import Reference


class ReferenceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reference, ReferenceAdmin)
