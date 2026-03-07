from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'location', 'address', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Item name ', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the item condition...', 'rows': 4, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Locality (optional)', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }