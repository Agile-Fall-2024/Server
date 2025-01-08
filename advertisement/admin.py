from django.contrib import admin

from advertisement.models import Advertisement, Category, Report


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username', 'category__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def mark_as_active(self, request, queryset):
        queryset.update(status=1)
        self.message_user(request, "Selected advertisements marked as ACTIVE.")

    def mark_as_resolved(self, request, queryset):
        queryset.update(status=2)
        self.message_user(request, "Selected advertisements marked as RESOLVED.")

    def mark_as_sold(self, request, queryset):
        queryset.update(status=3)
        self.message_user(request, "Selected advertisements marked as SOLD.")

    mark_as_active.short_description = "Mark selected advertisements as ACTIVE"
    mark_as_resolved.short_description = "Mark selected advertisements as RESOLVED"
    mark_as_sold.short_description = "Mark selected advertisements as SOLD"

    actions = [mark_as_active, mark_as_resolved, mark_as_sold]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title', 'description')
    ordering = ('title',)


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
