from django import forms
from .models import Service, UserService
from django.core.validators import RegexValidator



class NewServiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['service'].widget.attrs['class'] = 'form-control'
    
    alpha = RegexValidator(r'^[a-z]*$', 'Only characters are allowed.')
    address = forms.CharField(
        label="Endereço do servico",
        required=True,
        min_length=7,
        validators=[alpha]
    )
    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="(Nothing)")

    class Meta:
        model = UserService
        fields = ('service', 'address')
