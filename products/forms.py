from django import forms
from django_summernote.widgets import SummernoteWidget
from .widgets import CustomClearableFileInput
from .models import Product, Category, ProductReview


class ProductForm(forms.ModelForm):
    """
    From CI Boutique Ado
    """

    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'description': SummernoteWidget(),
        }

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ProductReviewForm(forms.ModelForm):
    """ Create a Review Form """
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
