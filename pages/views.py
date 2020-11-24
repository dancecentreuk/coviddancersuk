from django.shortcuts import render, redirect
from accounts.models import Candidate, CandidateImage, User, Employer
from .choices import location_choices, work_choices
from adverts.models import Advert
from .forms import CandidateReviewForm
from .models import CandidateReview
from django.contrib import messages
from django.db.models import Avg
from dance_classes.models import WeeklyDanceClass


def index(request):

    talents = Candidate.objects.all()
    jobs = Advert.objects.filter(is_posting=False).order_by('-created')[:5]
    postings = Advert.objects.filter(is_posting=True)[:5]
    dance_classes = WeeklyDanceClass.objects.filter(is_allowed=True).filter(is_published=True)

    context = {
        'talents': talents,
        'location_choices': location_choices,
        'work_choices': work_choices,
        'jobs': jobs,
        'postings': postings,
        'dance_classes': dance_classes

    }
    return render(request, 'pages/index.html', context)


def talent(request):
    talents = Candidate.objects.all()
    content = {

        'talents': talents,
        'location_choices': location_choices

    }
    return render(request, 'pages/talent.html', content)

def talent_detail(request, pk, first_name, last_name):
    talent = Candidate.objects.get(pk=pk, user__first_name=first_name, user__last_name=last_name)
    candidate_photos = CandidateImage.objects.filter(owner=pk)
    reviews = CandidateReview.objects.filter(candidate=pk).order_by('-created')
    average_reviews = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_reviews is not None:
        average_reviews = round(average_reviews, 1)
    form = CandidateReviewForm(request.POST or None)
    dance_classes = WeeklyDanceClass.objects.filter(author=talent)
    context = {

        'form':form,
        'talent': talent,
        'candidate_reviews': reviews,
        'candidate_photos': candidate_photos,
        'average_reviews': average_reviews,
        'dance_classes': dance_classes

    }
    return render(request, 'pages/talent_detail.html', context)


def search_talent(request):

    queryset_list = Candidate.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(experience__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(candidate_location=city)

    context = {

        'talents': queryset_list,
        'location_choices': location_choices,
        'values': request.GET

    }


    return render(request, 'pages/talent_search.html', context)



def employers(request):

    employers = Employer.objects.filter(is_company=True)
    context = {
        'employers': employers,
        'location_choices': location_choices
    }

    return render(request, 'pages/employers.html', context)


def employer_detail(request, pk, username):
    employer = Employer.objects.get(id=pk, user__username=username)
    adverts = Advert.objects.filter(is_posting=False).filter(author=employer.user)
    postings = Advert.objects.filter(is_posting=True).filter(author=employer.user)

    context = {
        'employer':employer,
        'adverts': adverts,
        'postings': postings
    }
    return render(request, 'pages/employer_detail.html', context)



def search_employer(request):

    queryset_list = Employer.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(company_name__icontains=keywords)



    context = {

        'employers': queryset_list,
        'values': request.GET

    }

    return render(request, 'pages/employers_search.html', context)


def add_candidate_review(request, id):
    if request.user.is_authenticated:
        candidate = Candidate.objects.get(id=id)

        if request.method == 'POST':
            form = CandidateReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.author = request.user
                data.candidate = candidate
                if data.candidate.user == request.user:
                    messages.error(request, 'You cant give your self a  review clever clogs')
                    return redirect('talent-detail', id, candidate.user.first_name, candidate.user.last_name)
                else:
                    data.save()

                    messages.success(request, 'Your review has now been posted')
                    return redirect('talent-detail', id, candidate.user.first_name, candidate.user.last_name)
            else:

                messages.error(request, 'There is a error in your review and it has not been posted')
                return redirect('talent-detail', id, candidate.user.first_name, candidate.user.last_name)
    else:
        return redirect('sign-in')



def edit_candidate_review(request, candidate_id, review_id):
    if request.user.is_authenticated:
        candidate = Candidate.objects.get(id=candidate_id)
        review = CandidateReview.objects.get(candidate=candidate, id=review_id)
        if request.user == review.author:
            if request.method == 'POST':
                form = CandidateReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = 'out of range ps select rating from 0 to 10'
                        return render(request, 'pages/edit_review.html', {'error': error, 'form':form})
                    else:
                        data.save()
                        return redirect('talent-detail', candidate.id, candidate.user.first_name, candidate.user.last_name)
            else:
                form = CandidateReviewForm(instance=review)
            context = {
                'form': form
            }
            return render(request, 'pages/edit_review.html', context)
        else:
            return redirect('talent-detail', candidate.id, candidate.user.first_name, candidate.user.last_name)

    else:
        return redirect('sign-in')
