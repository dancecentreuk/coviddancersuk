from django.shortcuts import render, redirect, get_object_or_404
from ..forms import CandidateSignUpForm, PhotoForm, EditDateForm, ImageUpdateForm
from pages.choices import gender_choices, location_choices
from ..models import CandidateImage, Candidate
from django.contrib import messages
from django.http import HttpResponse
from pages.choices import location_choices


def candidate_signup(request):
    form = CandidateSignUpForm
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST or None)




        if form.is_valid():
            form.save()
            messages.success(request, 'You are now registered and can log in')
            return redirect('sign-in')


    else:
        form = CandidateSignUpForm()

    context = {
        'form': form,
        'gender_choices':gender_choices,
        'location_choices': location_choices

    }
    return render(request, 'registration/candidate-signup.html', context)

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



