from django.contrib import admin
from .models import User, RaffleTicket, LuckyDraw

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(User, UserAdmin)


class RaffleTicketAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(RaffleTicket, RaffleTicketAdmin)


class LuckyDrawAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(LuckyDraw, LuckyDrawAdmin)
