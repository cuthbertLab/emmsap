from django.contrib import admin

from .main.models import Composer, Country

class ComposerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]

class CountryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]


admin.site.register(Composer, ComposerAdmin)
admin.site.register(Country, CountryAdmin)
