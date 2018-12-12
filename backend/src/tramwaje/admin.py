from django.contrib import admin

# Register your models here.
from .models import Linia
from .models import Motorniczy 
from .models import Praca 
from .models import Tramwaj 


admin.site.register(Linia)
admin.site.register(Motorniczy)
admin.site.register(Praca)
admin.site.register(Tramwaj)
