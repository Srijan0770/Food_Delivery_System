from django import forms
from .models import MenuItem, MenuCategory


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'category', 'name', 'description', 'price', 'image',
            'is_available', 'is_vegetarian', 'is_vegan', 'is_spicy',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs.setdefault('class', 'form-control')
