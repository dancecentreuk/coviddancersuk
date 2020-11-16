from django.shortcuts import render, redirect, get_object_or_404
from .models import Venue
from django.core.paginator import PageNotAnInteger, Paginator, Page, EmptyPage
from .forms import venueForm
from django.contrib import messages
from pages.choices import location_choices, age_choices

# Create your views here.



def venues(request):
    venues = Venue.objects.filter(is_published=True)

    paginator = Paginator(venues, 1)
    page = request.GET.get('page')
    paged_dance_classes = paginator.get_page(page)

    context = {
        'venues': paged_dance_classes,
        'location_choices': location_choices
    }
    return render(request, 'venues/venues.html',context)


def add_venue(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = venueForm(request.POST, request.FILES or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.author = request.user
                data.is_published = True
                data.save()
                return redirect('/')

        form = venueForm(request.POST or None)

        context = {
            'form': form

        }
        return render(request, 'venues/add_venue.html', context)

    else:
        return redirect('sign-in')


def venue_detail(request, pk, slug):

    venue = get_object_or_404(Venue, id=pk, slug=slug)

    context = {

        'venue': venue
    }
    return render(request, 'venues/venue_detail.html', context)

def edit_venue(request, pk, slug):
    if request.user.is_authenticated:
        venue = get_object_or_404(Venue, id=pk, slug=slug)
        if request.user == venue.author:
            if request.method == 'POST':
                form = venueForm(request.POST, request.FILES or None, instance=venue)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('venue-detail', venue.id, venue.slug)
            else:
                form = venueForm(instance=venue)
            context = {

                'form':form

            }
            return render(request, 'venues/add_venue.html', context)
        else:
            messages.error(request, ('you are not the creator of this veneu'))
            return redirect('venue-detail', venue.id, venue.slug)

    else:
        return redirect('sign-in')



def delete_venue(request, pk, slug):
    venue = Venue.objects.get(id=pk, slug=slug)
    if request.user == venue.author:
        venue.delete()
        messages.success(request, ('Venue listing has been deleted'))
        return redirect('venues')
    else:
        messages.error(request, ('you cant delete this venue'))
        return redirect('venue-detail', venue.id, venue.slug)


def venue_search(request):
    queryset_list = Venue.objects.all().filter(is_allowed=True).filter(is_published=True).order_by('-created')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(about__icontains=keywords)


    if 'mirrors' in request.GET:
        mirrors = request.GET['mirrors']
        if mirrors:
            queryset_list = queryset_list.filter(mirrors__exact=True)


    if 'music' in request.GET:
        music = request.GET['music']
        if music:
            queryset_list = queryset_list.filter(music_system__exact=True)


    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(location=city)

    context = {

        'venues': queryset_list,
        'location_choices':location_choices,
        'values': request.GET


    }
    return render(request, 'venues/search_venues.html', context)


# def delete_advert(request, pk, slug):
#     # get the advert
#     advert = Advert.objects.get(id=pk, slug=slug)
#     # delete the advert
#     advert.delete()
#     messages.success(request, ('item has been deleted'))
#     return redirect('adverts')

#
# def delete_advert2(request, pk, slug):
#     advert = Advert.objects.get(id=pk, slug=slug)
#     if request.method == 'POST':
#         advert.delete()
#         messages.success(request, ('item has been deleted'))
#         return redirect('profile')
#
#     context = {
#         'advert': advert
#     }
#     return render(request, 'adverts/delete_advert.html', context)


