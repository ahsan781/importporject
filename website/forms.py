from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        max_length=254
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = CustomUser.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError(
                "This email has already been registered. Try another email or reset your password."
            )
        return email