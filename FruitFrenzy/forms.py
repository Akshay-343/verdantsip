from django import forms
from .models import Reviews
from .models import Product


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review_title', 'review_content', 'review_rating', 'product_image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_description', 'product_ingredients', 'product_image',
                  'allergen']
