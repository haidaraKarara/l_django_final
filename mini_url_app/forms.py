from django import forms
from .models import MiniURL


class MiniURLForm(forms.ModelForm):
    class Meta:
        model = MiniURL
        fields = ('url','pseudo')

class ConnexionForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

