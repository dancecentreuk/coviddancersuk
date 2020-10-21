from django.shortcuts import render, redirect
from ..forms import EmployerSignUpForm, EmployerUpdateForm, EmployerImageUpdateForm
from pages.choices import gender_choices, location_choices
from ..models import Employer
from adverts.models import Advert
from django.http import HttpResponse
from django.contrib import messages



def employer_signup(request):
    form = EmployerSignUpForm
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'You are now registered and can log in')
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




