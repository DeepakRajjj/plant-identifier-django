from django import forms
from .models import PlantSale, Purchase

class PlantForm(forms.ModelForm):
    class Meta:
        model = PlantSale
        fields = ['name', 'image', 'description', 'price', 'quantity_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'quantity_available': forms.NumberInput(attrs={'min': 1})
        }
        labels = {
            'quantity_available': 'Quantity Available'
        }
        help_texts = {
            'quantity_available': 'Number of identical plants available for sale'
        }

class PurchaseForm(forms.ModelForm):
    # Override the quantity field to ensure it accepts values > 1
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500',
            'min': 1,
            'step': 1
        })
    )

    class Meta:
        model = Purchase
        fields = ['quantity', 'shipping_address', 'contact_phone']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full shipping address'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Enter your contact number'})
        }

    def clean_quantity(self):
        """Custom validation to ensure quantity is at least 1"""
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        return quantity
