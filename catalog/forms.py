from django import forms
from .models import Product, Version

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Применение crispy-форматирования
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})

    # Запрещенные слова для валидации
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in self.forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f"Название не должно содержать запрещенные слова, такие как: {word}.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in self.forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(f"Описание не должно содержать запрещенные слова, такие как: {word}.")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})