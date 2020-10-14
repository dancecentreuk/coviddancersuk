from django import forms
from .models import Advert

#advert add form

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ('title',  'body', 'fee', 'location')

class PostingForm(forms.ModelForm):
    date = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Birth'}))
    start_time = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'eg 3pm'}))
    finish_time = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'eg 5:30pm'}))

    class Meta:
        model = Advert
        fields = ('title',  'body', 'date', 'start_time', 'finish_time', 'fee', 'location')