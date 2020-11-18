from django import forms
from .models import WeeklyDanceClass, ClassImage, DanceClassReview
from pages.choices import dance_styles


class DanceClassForm(forms.ModelForm):


    dance_style_choice = forms.ChoiceField(
        label='Choose Dance Style',
        choices =dance_styles,
        initial='Select a dance',

    )
    start_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'type':'time', }))

    end_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'type': 'time', }))

    faq = forms.CharField(max_length=250, required=False, widget=forms.Textarea(
        attrs={ 'placeholder': 'There are aprox 15 people in a Class, Average age is 18, you dont need any experience for the beginners class etc .. '}))

    clothes = forms.CharField(required=False, label='What to wear to the dance class', max_length=250, widget=forms.TextInput(
        attrs={
            'placeholder': 'Clothing Loose comfortable clothing and socks if you dont have street shoes'}))

    drop_in = forms.CharField(required=False, label='Drop in Class or Booking required', max_length=250, widget=forms.TextInput(
        attrs={
            'placeholder': 'ie classes in  are on a drop in basis, no need to book'}))

    experience = forms.CharField(required=False, label='Experience required', max_length=250, widget=forms.TextInput(
        attrs={
            'placeholder': 'ie : No experience is required for the beginners class.'}))

    average_age = forms.CharField(required=False, label='Average age in class', max_length=250, widget=forms.TextInput(
        attrs={
            'placeholder': 'ie : Average age group in class is 20-35 yrs old'}))



    class Meta:
        model = WeeklyDanceClass
        fields = ('dance_style_choice', 'level', 'age_group', 'address', 'postcode',  'location', 'day', 'start_time', 'end_time', 'price',
                  'dance_class_image', 'dance_class_image_1', 'dance_class_image_2', 'dance_class_image_3', 'faq',
                    'clothes', 'experience', 'average_age', 'drop_in', 'about_dance_class', 'teacher',)




class DancePhotoForm(forms.ModelForm):
    class Meta:
        model = ClassImage
        fields = ('title',  'profile_image')



class DanceClassReviewForm(forms.ModelForm):



    class Meta:
        model = DanceClassReview
        fields = ('comment', 'rating')





