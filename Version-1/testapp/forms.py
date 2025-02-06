from django import forms
from testapp.models import add_Form

class add_product_form(forms.ModelForm):
    class Meta:
        model = add_Form
        
        # exclude = ["product_name","details"]
        fields = ["form_name","form_category","form_image","ocr_choices","lang_ocr"]
