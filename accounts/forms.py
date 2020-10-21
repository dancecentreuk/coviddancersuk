from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import User, Candidate, Employer, CandidateImage
from pages.choices import gender_choices, location_choices



class CandidateSignUpForm(UserCreationForm):
    mobile = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class':'form-control', 'placeholder':'Mobile'}))
    date_of_birth = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type':'date',  'placeholder': 'Date of Birth'}))
    gender = forms.CharField(widget=forms.Select(choices=gender_choices))
    candidate_location = forms.CharField(widget=forms.Select(choices=location_choices))
    password1 = forms.CharField(max_length=250, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=250, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password Confirm'}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'mobile',
                  'gender', 'candidate_location',]


        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),

        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Ps supply  a different email address")
        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_candidate = True
        user.save()
        candidate = Candidate.objects.create(user=user,
                                             mobile=self.cleaned_data.get('mobile'),
                                             date_of_birth =self.cleaned_data.get('date_of_birth'),
                                             gender=self.cleaned_data.get('gender'),
                                             candidate_location = self.cleaned_data.get('candidate_location')
                                             )

        return user


class EmployerSignUpForm(UserCreationForm):
    mobile = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile'}))
    password1 = forms.CharField(max_length=250, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=250, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password Confirm'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',  'mobile',
                    ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),

        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use. Ps supply  a different email address")
        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()
        employer = Employer.objects.create(user=user,
                                             mobile=self.cleaned_data.get('mobile'),
                                             )

        return user

class PhotoForm(forms.ModelForm):
    class Meta:
        model = CandidateImage
        fields = ('title',  'profile_image')


class DateInput(forms.DateInput):
    input_type = 'date'


class EditDateForm(forms.Form):
    edit_date_of_birth = forms.DateField(widget=DateInput)


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('profile_image', )

class EmployerUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('mobile', 'is_company', 'company_name', 'company_email')


class EmployerImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('profile_image', )