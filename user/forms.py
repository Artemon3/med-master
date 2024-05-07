from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ProfilePatient, ProfileDoctor
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, AuthenticationForm, UserCreationForm, \
    UsernameField, PasswordChangeForm


class ProfilePatientForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Иван", })
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Иванов"})
    )
    patronymic = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Иванович"})
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "+7(___)-___-__-__"})
    )
    insurance = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "СНИЛС"})
    )
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': "Email"})
    # )
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': "Дата рождения"})
    )
    residential_address = forms.CharField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': "Адрес проживания"})
    )

    class Meta:
        model = ProfilePatient
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'insurance', 'date', 'residential_address']


class RegistrationForm(ProfilePatientForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['confirm_password'].label = 'Подтверждение пароля'
        self.fields['password'].label = 'Пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['date'].label = 'Дата рождения'
        self.fields['phone'].label = 'Моб.телефон'
        self.fields['residential_address'].label = 'Адрес проживания'
        self.fields['email'].label = 'Email'
        self.fields['insurance'].label = 'Страховой полис'

    def clean_email(self):
        email = self.cleaned_data['email']
        if ProfilePatient.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый ящик уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if ProfilePatient.objects.filter(Q(username=username) | Q(email=username)).exists():
            raise forms.ValidationError('Данный логин уже зарегистрирован')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    class Meta:
        model = ProfilePatient
        fields = ['username', 'password',
                  'confirm_password', 'first_name',
                  'last_name', 'patronymic', 'date', 'residential_address',
                  'phone', 'email', 'insurance', ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'type': 'password',
            'class': 'form-control',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин или Email'
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = ProfilePatient
        fields = ['username', 'password']


class PasswordResetUserForm(PasswordResetForm):
    email = forms.EmailField(
        label="Адрес электронной почты",
        max_length=150,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Email"}
        )
    )


class SetPasswordUserForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'type': 'password',
            'class': 'form-control',
        }),
        strip=False,

    )
    new_password2 = forms.CharField(
        label="Подтвердите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'type': 'password',
            'class': 'form-control',
        }),
    )


class PasswordChangeUserForm(SetPasswordUserForm, PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'type': 'password',
            'class': 'form-control',
        }),
    )
