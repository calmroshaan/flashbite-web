from django import forms
from .models import SurpriseBag

class SurpriseBagForm(forms.ModelForm):
    class Meta:
        model = SurpriseBag
        fields = ['title', 'description', 'original_price', 'discounted_price', 'pickup_start', 'pickup_end', 'quantity_left', 'image']
        
        # This makes the form look beautiful using Bootstrap classes
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 Large Pizzas'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'pickup_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'quantity_left': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # The Security Check: Block images larger than 2MB
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024: # 2 Megabytes
                raise forms.ValidationError("Image file is too large ( > 2MB ). Please upload a smaller image.")
        return image