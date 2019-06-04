from django.contrib import admin
from .models import Piece, Composer, Country

class CountryAdmin(admin.ModelAdmin):
    model = Country

admin.site.register(Piece)
admin.site.register(Country, CountryAdmin)
admin.site.register(Composer)
