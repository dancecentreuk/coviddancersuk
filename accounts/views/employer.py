from django.shortcuts import render, redirect
from ..forms import EmployerSignUpForm, EmployerUpdateForm, EmployerImageUpdateForm
from pages.choices import gender_choices, location_choices
from ..models import Employer
from adverts.models import Advert
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
import threading
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from ..utils import token_generator
from accounts.models import User




class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

def employer_signup(request):
    form = EmployerSignUpForm
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST or None)





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
        form = EmployerSignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/employer-signup.html', context)


def employer_profile(request):
    employer = request.user.employer
    adverts = Advert.objects.filter(is_posting=False).filter(author=request.user).order_by('-created')
    adverts_count = adverts.count()
    postings = Advert.objects.filter(is_posting=True).filter(author=request.user)
    postings_count = postings.count()
    employer_update_form = EmployerUpdateForm(request.POST or None, instance=request.user.employer)
    employer_image_form = EmployerImageUpdateForm(request.POST or None)
    context = {
        'employer' : employer,
        'employer_update_form': employer_update_form,
        'adverts': adverts,
        'adverts_count': adverts_count,
        'postings': postings,
        'postings_count': postings_count,
        'employer_image_form': employer_image_form


    }
    return render(request, 'accounts/employer_profile.html', context)


def update_company_profile(request, pk):
    employer = Employer.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployerUpdateForm(request.POST or None, instance=request.user.employer)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('employer-profile')
    else:
        return redirect('sign-in')


 # if request.method =='POST':
 #        candidate = Candidate.objects.get(pk=pk)
 #        bio = request.POST['bio']
 #        candidate.bio = bio
 #        candidate.save()
 #    return redirect('candidate-profile')


def update_company_bio(request, pk):
    if request.method == 'POST':
        employer = Employer.objects.get(pk=pk)
        employer.company_info = request.POST['company_info']
        employer.save()
        return redirect('employer-profile')



def update_profile_picture(request, pk):
    if request.method == 'POST':
        new_image_form = EmployerImageUpdateForm(request.POST, request.FILES, instance=request.user.employer)
        if new_image_form.is_valid():
            data = new_image_form.save(commit=False)
            data.save()
            return redirect('employer-profile')




