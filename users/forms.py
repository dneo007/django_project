from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fc = forms.BooleanField(required=False, label='Enable FaceID')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'fc']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = '<small>Your password can’t be too similar to your other personal ' \
                                             'information.<br>Your password must contain at least 8 ' \
                                             'characters.<br>Your password can’t be a commonly used password.<br>Your ' \
                                             'password can’t be entirely numeric. <br><br></small> '
        for fieldname in ['username', 'password2']:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        help_texts = {'username': (None)}
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):

    org = forms.CharField(required=False, max_length=100, label='Organisation')
    contactno = forms.IntegerField(required=False, label='Contact Number')

    class Meta:
        model = Profile
        fields = ['org', 'contactno', 'country', 'image']


class FacialRecForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fc']


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
