from django.contrib import admin

from .models import Piece, Composer, Country

admin.site.register(Piece)
admin.site.register(Composer)
admin.site.register(Country)
