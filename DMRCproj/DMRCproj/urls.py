
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from project.views import ChangePasswordView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("project.urls")),
    path('password-change/', ChangePasswordView.as_view(), name='password_change')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "DMRC Admin"
admin.site.site_title = "DMRC Admin Portal"
admin.site.index_title = "Welcome to DMRC File Sharing application"
