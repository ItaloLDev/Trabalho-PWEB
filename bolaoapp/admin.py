from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Partida
from .models import Jogador

class JogadorInline(admin.StackedInline):
    model = Jogador
    can_delete = False
    verbose_name_plural = 'Jogadores'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (JogadorInline,)


admin.site.register(Partida)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)