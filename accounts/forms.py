from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        label="Role"
    )
    email = forms.EmailField(required=True, label="Email",
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'you@email.com'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': '••••••••'})