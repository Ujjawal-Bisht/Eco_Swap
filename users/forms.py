# pyrefly: ignore [missing-import]
from django import forms
# pyrefly: ignore [missing-import]
from django.core.exceptions import ValidationError
from .models import User

MAX_PROFILE_IMAGE_SIZE_MB = 5


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'location', 'sustainability_interests']
        widgets = {
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. South Delhi'
            }),
            'sustainability_interests': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'e.g. composting, upcycling, zero-waste living'
            }),
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            max_size_bytes = MAX_PROFILE_IMAGE_SIZE_MB * 1024 * 1024
            if image.size > max_size_bytes:
                raise ValidationError(
                    f"Image file too large. Maximum size is {MAX_PROFILE_IMAGE_SIZE_MB}MB."
                )
        return image