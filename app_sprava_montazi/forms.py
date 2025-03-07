from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Uživatelské jméno'
        }),
        label=''  # prázdný label, nebude se vykreslovat
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Heslo'
        }),
        label=''
    )
