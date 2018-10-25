from django.contrib import admin
from .models import MiniURL,Eleve,Lieu,Restaurant
# Register your models here.
class MiniURLAdmin(admin.ModelAdmin):

    # Configuration de la liste d'articles
    list_display   = ('url', 'code', 'date', 'pseudo','nb_acces')
    list_filter    = ('pseudo', )
    date_hierarchy = 'date'
    ordering       = ('-date', )
    search_fields  = ('url',)

admin.site.register(MiniURL,MiniURLAdmin)
admin.site.register(Eleve)
admin.site.register(Lieu)
admin.site.register(Restaurant)
