from django import forms


class AvatarForm(forms.Form):
    avatarid = forms.CharField(
        max_length=20, 
        label='Avatar ID', 
        required=True, 
        error_messages={
            'required': 'このフィールドは必須です。'  # "This field is required."
        }
    )
    image = forms.ImageField(
        label='Upload Avatar', 
        required=True, 
        error_messages={
            'required': '選択されていません'  # "Not selected."
        }
    )
    # Optionally, you can add a clean method to validate the image type or size
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Example: Check if the image size is greater than 2 MB
            if image.size > 2 * 1024 * 1024:  # Size in bytes
                raise forms.ValidationError("Image size must be less than 2 MB.")
            # Add other validations as needed
        return image