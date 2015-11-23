from django import forms

from mate.models import Mate


class BecomeMatesForm(forms.ModelForm):
    class Meta:
        model = Mate
        fields = '__all__'
