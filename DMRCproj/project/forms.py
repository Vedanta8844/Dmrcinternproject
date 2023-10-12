
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import UploadedFile, FileShare, Contact
from django.forms import EmailInput, TextInput
from django.contrib.auth.forms import UserChangeForm


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)


class FileShareForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label='Select User',
        empty_label='Choose a user',
    )

    class Meta:
        model = FileShare
        fields = ['receiver', 'file']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['username', 'email', 'desc']
        widgets = {
            'desc': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your complaint '
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            })
        }


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already in use. Please choose a different one.")
        return username


class UpdateProfile(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('profilepic', 'full_name', 'username', 'email')
