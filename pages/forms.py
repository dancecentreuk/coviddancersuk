from django import forms
from .models import CandidateReview
from django.core.exceptions import ValidationError


class CandidateReviewForm(forms.ModelForm):



    class Meta:
        model = CandidateReview
        fields = ('comment', 'rating')


