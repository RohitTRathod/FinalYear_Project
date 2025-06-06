from django import forms

class CropInputForm(forms.Form):
    N = forms.FloatField()
    P = forms.FloatField()
    K = forms.FloatField()
    temperature = forms.FloatField()
    humidity = forms.FloatField()
    ph = forms.FloatField()
    rainfall = forms.FloatField()
