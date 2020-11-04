from django import forms
from .models import WeeklyDanceClass
from pages.choices import dance_styles


class DanceClassForm(forms.ModelForm):


    dance_style_choice = forms.ChoiceField(
        label='Chooes Dance Style',
        choices =dance_styles,
        initial='Select a dance',

    )
    start_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'type':'time', }))

    end_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'type': 'time', }))

    faq = forms.CharField(max_length=250, widget=forms.Textarea(
        attrs={ 'placeholder': 'There are aprox 15 people in a Class, Average age is 18, you dont need any experience for the beginners class etc .. '}))





    class Meta:
        model = WeeklyDanceClass
        fields = ('dance_style_choice', 'level', 'age_group', 'address', 'postcode',  'location', 'day', 'start_time', 'end_time', 'price',  'dance_class_image', 'faq',
                    'about_dance_class', 'teacher',)




