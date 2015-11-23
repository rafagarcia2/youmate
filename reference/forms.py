from django import forms

from reference.models import Reference


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = '__all__'
