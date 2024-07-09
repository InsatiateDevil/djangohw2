from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, EmailInput, ModelForm
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'phone_number', 'avatar', 'country']


class PasswordRecoveryForm(Form):
    email = EmailField(
        required=True,
        widget=EmailInput(
            attrs={
                'placeholder': 'Введите адрес электронной почты',
                'class': 'form-control text-center',
            }
        ),
    )
