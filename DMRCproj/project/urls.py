from django.contrib import admin
from django.urls import path
from project import views
# from .views import FileUploadView

from .views import ChangePasswordView
urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('contact/', views.contact, name="contact"),
    path('upload/', views.upload, name="upload"),
    path('uploadedfiles/', views.uploadedfiles, name="uploadedfiles"),
    path('signup/', views.signupUser, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('share/', views.share, name="share"),
    path('updateprofile/', views.updateprofile, name="updateprofile"),
    # path('3/password/', ChagePasswordView.as_view(), name="passchange"),
    path('inbox/', views.inbox, name="inbox")


]
