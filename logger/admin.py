from django.contrib import admin

from logger.models import Log

# Register your models here.
class logAdmin(admin.ModelAdmin):
    list_display = ('action', 'related_id', 'created')

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Log, logAdmin)