from django import forms
from .models import BotSettings, ContactInfo, BotInfo

class BotSettingsForm(forms.ModelForm):
    class Meta:
        model = BotSettings
        fields = ['key', 'value', 'file', 'description']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['title', 'contact_type', 'value', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BotInfoForm(forms.ModelForm):
    class Meta:
        model = BotInfo
        fields = ['title', 'content', 'image', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
