
from django.contrib import admin
# from .models import File
from .models import UploadedFile, FileShare, Contact, CustomUser

# Register your models here.
# admin.site.register(File)
# admin.site.register(FilePermission)


# class FileAdmin(admin.ModelAdmin):
#     list_display = ('file', 'user', 'file_name',
#                     'file_size', 'upload_date', 'is_private')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')


@admin.register(FileShare)
class FileShareAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'file', 'shared_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'desc')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'username', 'password', 'profilepic')
