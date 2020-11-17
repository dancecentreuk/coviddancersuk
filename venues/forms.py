from django import forms
from .models import Venue, VenueReview


class venueForm(forms.ModelForm):



    flooring = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={
            'placeholder': 'ie wooden floor,  harlequinn, carpetted'}))

    faq = forms.CharField(max_length=250, widget=forms.Textarea(
        attrs={
            'placeholder': 'There are aprox 15 people in a Class, Average age is 18, you dont need any experience for the beginners class etc .. '}))



    price = forms.FloatField( widget=forms.NumberInput(attrs={'placeholder': 'Cost per Hour'}))

    class Meta:
        model = Venue
        fields = ('venue_name', 'address', 'location', 'postcode','size_width_ft', 'size_length_ft', 'flooring', 'mirrors',
                  'music_system', 'price', 'contact_person', 'contact_number', 'contact_email', 'about', 'faq',  'venue_image',
                  'venue_image_1', 'venue_image_2', 'venue_image_3')


class VenueReviewForm(forms.ModelForm):

    class Meta:
        model = VenueReview
        fields = ('comment', 'rating')