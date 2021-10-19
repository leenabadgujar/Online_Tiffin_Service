from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, authenticate, UserChangeForm


class Registration(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"class": 'form-login placeicon', "placeholder": 'Enter Password'}))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"class": 'form-login placeicon', "placeholder": 'Re-enter Password'}))

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'number', 'city',
                  'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-login placeicon', "placeholder": 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-login placeicon', "placeholder": 'Enter your email'}),
            'number': forms.NumberInput(attrs={'class': 'form-login placeicon', "placeholder": 'Enter your number'}),
            'city': forms.TextInput(attrs={'class': 'form-login placeicon', "placeholder": 'Enter your City'}),
        }


class Login(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"class": 'form-login placeicon', "placeholder": 'Enter Password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-login placeicon', "placeholder": 'Enter your email'})
        }

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid Login')

# class ProfileForm(UserChangeForm):
#     password = None
#     class Meta:
#         model = CustomUser
#         fields = ('name','user_image','position','description')
#         labels = {
#             'position':'Role',
#             'description':'About Yourself'
#         }
