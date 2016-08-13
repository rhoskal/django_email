from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms

from .models import Client

class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user

    class Meta:
        model = Client

        fields = (
            'email',
        )

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client

        fields = (
            'email',
            'password',
        )

    def clean_password(self):
        return self.initial['password']
