from django import forms
from .models import StoreUser

# class UserSignUpForm(forms.ModelForm):
#     class Meta:
#         model = StoreUser
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'contact_number']
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'contact_number': forms.TextInput(attrs={'class': 'form-control', 'pattern': r'^\+92\d{10}$',  # Example for +92 country code followed by 10 digits
#                 'placeholder': '+921234567890',}),
#         }

class UserSignUpForm(forms.ModelForm):
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'^\+92\d{10}$',
            'placeholder': '+921234567890',
        })
    )

    class Meta:
        model = StoreUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.startswith('+92') or not contact_number[3:].isdigit() or len(contact_number) != 13:
            raise forms.ValidationError("Enter a valid contact number in the format +92XXXXXXXXXX.")
        return contact_number
