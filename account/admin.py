from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'otp', 'otp_expiry', 'bio_snippet', 'address_snippet')

    search_fields = ('user__username', 'user__email', 'phone_number', 'bio', 'address')

    list_filter = ('otp_expiry',)

    readonly_fields = ('otp', 'otp_expiry')

    def bio_snippet(self, obj):
        return obj.bio[:15] + '...' if obj.bio and len(obj.bio) > 50 else obj.bio

    bio_snippet.short_description = 'Bio'

    def address_snippet(self, obj):
        return obj.address[:15] + '...' if obj.address and len(obj.address) > 50 else obj.address

    address_snippet.short_description = 'Address'
