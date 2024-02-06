from django.contrib import admin
from .models import Tasks

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'created', 'completed')
    list_filter = ('created', 'completed')
    search_fields = ('description', )

admin.site.register(Tasks, TaskAdmin)