from django import forms
from django.core.exceptions import ValidationError

from .models import Product


# Запрещённые слова (проверяются без учёта регистра)
FORBIDDEN_WORDS = {
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
    'обман', 'полиция', 'радар'
}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'category',
            'price',
            'image',
            'is_available',
            'is_published',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            # Базовый класс для большинства инпутов
            if hasattr(widget, 'input_type') and widget.input_type == 'checkbox':
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-control').strip()

    def _validate_forbidden_words(self, value: str, field_label: str) -> str:
        if not value:
            return value
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(
                    f"В поле '{field_label}' нельзя использовать слово: {word}")
        return value

    def clean_name(self) -> str:
        name = self.cleaned_data.get('name')
        return self._validate_forbidden_words(name, 'Название')

    def clean_description(self) -> str:
        description = self.cleaned_data.get('description')
        return self._validate_forbidden_words(description, 'Описание')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Проверяем размер файла (<= 5 МБ)
        max_bytes = 5 * 1024 * 1024
        if getattr(image, 'size', 0) > max_bytes:
            raise ValidationError('Изображение должно быть не больше 5 МБ')

        # Проверяем формат по content_type
        content_type = getattr(getattr(image, 'file', None), 'content_type', None)
        if content_type not in {'image/jpeg', 'image/png'}:
            raise ValidationError('Допустимые форматы изображений: JPEG или PNG')

        return image


