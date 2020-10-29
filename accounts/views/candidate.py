from django.shortcuts import render, redirect, get_object_or_404
from ..forms import CandidateSignUpForm, PhotoForm, EditDateForm, ImageUpdateForm
from pages.choices import gender_choices, location_choices
from ..models import CandidateImage, Candidate
from django.contrib import messages
from django.http import HttpResponse
from pages.choices import location_choices
from django.core.mail import EmailMessage
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from ..utils import token_generator
from accounts.models import User
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

def candidate_signup(request):
    form = CandidateSignUpForm
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST or None)




        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')


            user = User.objects.get(email=email)

            print(user.pk)


            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))



            domain = get_current_site(request).domain
            link = reverse('candidate-activate', kwargs={
                'uidb64':uidb64, 'token':token_generator.make_token(user)})

            activate_url = 'http://'+domain+link

            email_subject = 'Activate your account'
            email_body = 'Hi '+ user.first_name+ ' Ps use the link below to activate your account\n' + activate_url
            email_address = form.cleaned_data.get('email')
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@dance.com',
                [email_address]

            )
            EmailThread(email).start()



            # # Send email
            # send_mail(
            #   'Property Listing Inquiry',
            #   'There has been an inquiry for  Sign into the admin panel for more info',
            #   'traversy.brad@gmail.com',
            #   [realtor_email, 'techguyinfo@gmail.com'],
            #   fail_silently=False
            # )
            messages.success(request, 'You are now registered ps check your email to activate your account')
            return redirect('sign-in')


    else:
        form = CandidateSignUpForm()

    context = {
        'form': form,
        'gender_choices':gender_choices,
        'location_choices': location_choices

    }
    return render(request, 'registration/candidate-signup.html', context)


class CandidateVerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('sign-in'+'?message='+'User allreaedy activated' )

            if user.is_active:
                return redirect('sign-in')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated sucessfully')
            return redirect('sign-in')

        except Exception as e:
            pass


        return redirect('sign-in')



def candidate_profile(request):

    candidate = request.user.candidate
    photos = CandidateImage.objects.filter(owner__user=request.user)
    form = PhotoForm(request.POST or None)
    image_form = ImageUpdateForm(request.POST or None)
    context = {
        'location_choices': location_choices,
        'photos': photos,
        'candidate': candidate,
        'form': form,
        'image_form': image_form
    }

    return render(request, 'accounts/candidate_profile.html', context)





def candidate_location_update(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    if candidate.pk != request.user.candidate.pk:
        messages.error(request, f'This is not your profile')
        return redirect('candidate-profile')
    else:

        if request.method =='POST':
            candidate = Candidate.objects.get(pk=pk)
            location = request.POST['candidate_location']
            candidate.candidate_location = location
            candidate.save()
        return redirect('candidate-profile')


def candidate_birthday_update(request, pk):
    if request.method =='POST':
        candidate = Candidate.objects.get(pk=pk)
        date_of_birth = request.POST['date_of_birth']
        candidate.date_of_birth = date_of_birth
        candidate.save()
    return redirect('candidate-profile')

def candidate_bio_update(request, pk):
    if request.method =='POST':
        candidate = Candidate.objects.get(pk=pk)
        bio = request.POST['bio']
        candidate.bio = bio
        candidate.save()
    return redirect('candidate-profile')


def candidate__update(request, pk):
    if request.method =='POST':
        bio = request.POST['bio']
        print(bio)
        candidate = Candidate.objects.update(bio=bio)
    return redirect('candidate-profile')


def candidate_experience_update(request, pk):
    if request.method =='POST':
        candidate = Candidate.objects.get(pk=pk)
        experience = request.POST['experience']
        candidate.experience = experience
        candidate.save()
    return redirect('candidate-profile')

def candidate_delete_photos(request, pk):
    photo = CandidateImage.objects.get(id=pk)
    photo.delete()
    messages.success(request, ('photo has been deleted'))
    return redirect('candidate-profile')

def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES or None)

        if form.is_valid():
            data=form.save(commit=False)
            data.owner = request.user.candidate
            data.save()
            return redirect('candidate-profile')
        else:
            return HttpResponse(request, 'unable to save')

def add_photo_2(request):

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES or None)

        if form.is_valid():
            data=form.save(commit=False)
            data.owner = request.user.candidate
            data.save()
            return redirect('candidate-profile')

    form = PhotoForm(request.POST or None)

    context = {
        'form': form
    }

    return render(request, 'accounts/add-photo.html', context)





def update_candidate_profile_picture(request, pk):
    if request.method == 'POST':
        new_image_form = ImageUpdateForm(request.POST, request.FILES, instance=request.user.candidate)
        if new_image_form.is_valid():
            data = new_image_form.save(commit=False)
            data.save()
            return redirect('candidate-profile')






# def create_advert(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#           form = AdvertForm(request.POST, request.FILES)
#           if form.is_valid():
#               obj = form.save(commit=False)
#               obj.author = request.user
#               obj.save()
#               return redirect('/store/adverts/')
#
#
#
#     form = AdvertForm()
#
#
#     context = {
#
#         'form': form
#
#     }
#     return render(request, 'store/advert_create.html', context)
#





# def posting_create(request):
#     if request.method == 'POST':
#         form = PostingForm(request.POST or None)
#
#         #check if form is valid
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.author = request.user.employer
#             data.is_posting = True
#             data.save()
#
#             # redirect to created post
#             return redirect ('/')
#     else:
#         form = PostingForm()
#     context = {
#         'form':form
#
#     }
#     return render(request, 'adverts/create_advert.html', context)



