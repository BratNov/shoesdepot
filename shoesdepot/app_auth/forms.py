from django.contrib.auth import forms as auth_forms, get_user_model
from ..common import form_mixins
from django import forms
from .models import Profile

UserModel = get_user_model()


class RegisterUserForm(form_mixins.BootstrapFormMixin, auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'password1', 'password2')
        labels = {
            'email': 'Email address',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class LoginUserForm(form_mixins.BootstrapFormMixin, auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class UpdateUserForm(form_mixins.BootstrapFormMixin, auth_forms.UserChangeForm):
    password = None

    class Meta(auth_forms.UserChangeForm):
        model = UserModel
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class ChangePasswordForm(form_mixins.BootstrapFormMixin, auth_forms.PasswordChangeForm):
    class Meta(auth_forms.PasswordChangeForm):
        model = UserModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class ProfileForm(form_mixins.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'country', 'city', 'postcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        self.__init_fields__()
