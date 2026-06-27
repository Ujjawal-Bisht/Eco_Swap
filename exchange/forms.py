# pyrefly: ignore [missing-import]
from django import forms
# pyrefly: ignore [missing-import]
from django.core.exceptions import ValidationError
from .models import Item

MAX_ITEM_IMAGE_SIZE_MB = 5
MIN_TITLE_LENGTH = 3
MIN_DESCRIPTION_LENGTH = 10


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'location', 'address', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Item name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the item condition...',
                'rows': 4,
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Locality (optional)', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < MIN_TITLE_LENGTH:
            raise ValidationError(f"Title must be at least {MIN_TITLE_LENGTH} characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) < MIN_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Please provide a bit more detail (at least {MIN_DESCRIPTION_LENGTH} characters)."
            )
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size_bytes = MAX_ITEM_IMAGE_SIZE_MB * 1024 * 1024
            if image.size > max_size_bytes:
                raise ValidationError(
                    f"Image file too large. Maximum size is {MAX_ITEM_IMAGE_SIZE_MB}MB."
                )
        return image