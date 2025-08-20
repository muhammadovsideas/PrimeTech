# forms.py
from django import forms
from django.core.exceptions import ValidationError
from packaging.utils import _

from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        product = self.cleaned_data.get("product")

        if product and quantity:
            if product.amount < quantity:
                raise ValidationError(
                    _("Mahsulot yetarli emas! Omborda faqat {} dona bor.").format(product.amount)
                )
        return quantity