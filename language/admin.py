from django.contrib import admin

from language.models import Language


class LanguageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)
