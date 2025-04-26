from django.contrib import admin

from .models import App, UploadedFile, GraphicsSettings

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name',)


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name_display', 'ip_address_display', 'upload_time_display')
    list_display_links = None 
    search_fields = ('file_name', 'ip_address')
    list_filter = ('upload_time',)
    list_per_page = 20

    @admin.display(description="Имя файла")  
    def file_name_display(self, obj):
        return obj.file_name  

    @admin.display(description="IP-адрес")  
    def ip_address_display(self, obj):
        return obj.ip_address  

    @admin.display(description="Дата загрузки")  
    def upload_time_display(self, obj):
        return obj.upload_time  

    def has_add_permission(self, request):
        return False  

    def has_change_permission(self, request, obj=None):
        return False  

    def has_delete_permission(self, request, obj=None):
        return False  
    
admin.site.register(GraphicsSettings)

