from django.contrib import admin
from .models import Event, Favorite, EventType

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_event_type_name', 'date', 'location', 'user', 'created_at')
    list_filter = ('event_type', 'date')  # ForeignKey হিসেবে সঠিকভাবে কাজ করবে
    search_fields = ('title', 'location')

    def get_event_type_name(self, obj):
        return obj.event_type.name if obj.event_type else "None"
    get_event_type_name.short_description = "Event Type"

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Event, EventAdmin)
admin.site.register(Favorite)
admin.site.register(EventType, EventTypeAdmin)