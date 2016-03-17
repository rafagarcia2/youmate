from django.contrib import admin

from core.models import CoreUser, Profile


class CoreUserAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(CoreUser, CoreUserAdmin)
admin.site.register(Profile, ProfileAdmin)
