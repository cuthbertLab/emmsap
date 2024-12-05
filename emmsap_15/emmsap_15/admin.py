from django.contrib import admin

from .models import Piece, Composer, Country, SkipGroupCategory, SkipGroup, SkipPiece

admin.site.register(Piece)
admin.site.register(Composer)
admin.site.register(Country)
admin.site.register(SkipGroupCategory)
admin.site.register(SkipGroup)
admin.site.register(SkipPiece)

