from django.forms import ModelForm
from .models import keys

class publicKeyUploadForm(ModelForm):
    class Meta:
        model = keys
        fields = ['public_key']


class priKeyUploadForm(ModelForm):
    class Meta:
        model = keys
        fields = ['private_key']
