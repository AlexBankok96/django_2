from django.forms import ModelForm, forms, BooleanField
from catalog.models import Product, Version

class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Product
        exclude = ("owner",)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['name']

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Данное наименование не подходит')

        return cleaned_data

    def clean_product_description(self):
        cleaned_data = self.cleaned_data['description']

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Данное описание не подходит')

        return cleaned_data

class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'name', 'version_flag')

    def clean_version_number(self):
        cleaned_data = self.cleaned_data['version_number']
        if cleaned_data < 1:
            raise forms.ValidationError("Номер версии должен быть больше или равен 1.")
        return cleaned_data

from django import forms
from catalog.models import Product

class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'purchase_price', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
