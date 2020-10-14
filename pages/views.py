from django.shortcuts import render
from accounts.models import Candidate, CandidateImage, User, Employer
from .choices import location_choices, work_choices
from adverts.models import Advert


def index(request):

    talents = Candidate.objects.all()
    jobs = Advert.objects.filter(is_posting=False).order_by('-created')[:5]
    postings = Advert.objects.filter(is_posting=True)[:5]

    context = {
        'talents': talents,
        'location_choices': location_choices,
        'work_choices': work_choices,
        'jobs': jobs,
        'postings': postings

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
    context = {

        'talent': talent,
        'candidate_photos': candidate_photos

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
