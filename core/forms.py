from django import forms
from .models import StoreUser
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class StoreUserForm(forms.ModelForm):
    class Meta:
        model = StoreUser
        fields = ['contact_number']
        widgets = {
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^\+92\d{10}$', 
                'placeholder': '+921234567890',}),
        }
        
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if StoreUser.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("This contact number is already registered.")
        if not contact_number.startswith('+92') or not contact_number[3:].isdigit() or len(contact_number) != 13:
            raise forms.ValidationError("Enter a valid contact number in the format +92XXXXXXXXXX.")
        return contact_number
