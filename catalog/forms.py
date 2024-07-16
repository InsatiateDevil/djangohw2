from django.forms import ModelForm, forms, BooleanField

from catalog.models import Product, Version, Blog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа",
                           "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in forbidden_words:
            if word in product_name.lower():
                raise forms.ValidationError(
                    "Введенное название содержит запрещенные слова")
        return product_name

    def clean_description(self):
        description = self.cleaned_data['description']
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа",
                           "дешево", "бесплатно", "обман", "полиция", "радар"]
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(
                    "Введенное описание содержит запрещенные слова")
        return description


class ProductModerationForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'description', 'category',)


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'preview_image',)


class BlogModerationForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ('is_published',)
