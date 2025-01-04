from django.contrib import admin

from advertisement.models import Advertisement, Category, Report


# Register your models here.
@admin.register(Advertisement)
class AdvertiseAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'user', 'reason', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('advertisement__title', 'user__username', 'reason')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_read=False)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected reports marked as read.")

    mark_as_read.short_description = "Mark selected reports as read"

    actions = [mark_as_read]
