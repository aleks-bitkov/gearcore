from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django import forms as d_forms
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": d_forms.EmailField}


class UserAdminCreationForm(admin_forms.BaseUserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": d_forms.EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    first_name = d_forms.CharField()
    last_name = d_forms.CharField()
    phone_number = d_forms.CharField()

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save()
        return user

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        phone_length = len(phone)
        must_numbers = 10

        if not phone.isdigit():
            raise d_forms.ValidationError(_("Phone number can`t contains letters."))

        if phone_length > must_numbers or phone_length < must_numbers:
            raise d_forms.ValidationError(
                _("Phone number must contains only ten numbers"),
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "last_name",
            "patronymic",
            "phone_number",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "patronymic": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patronymic"].required = False
        self.fields["image"].required = False


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
