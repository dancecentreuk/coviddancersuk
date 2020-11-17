from django.shortcuts import render, redirect, get_object_or_404
from .models import Venue, VenueReview
from django.core.paginator import PageNotAnInteger, Paginator, Page, EmptyPage
from .forms import venueForm, VenueReviewForm
from django.contrib import messages
from pages.choices import location_choices, age_choices
from django.db.models import Avg

# Create your views here.



def venues(request):
    venues = Venue.objects.filter(is_published=True)

    paginator = Paginator(venues, 20)
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
    venue_review = VenueReview.objects.filter(venue=pk).order_by('-created')
    average_reviews = venue_review.aggregate(Avg('rating'))['rating__avg']
    if average_reviews is not None:
        average_reviews = round(average_reviews, 1)

    context = {

        'venue': venue,
        'venue_review': venue_review,
        'average_reviews': average_reviews
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





def add_venue_review(request, id, slug):
    if request.user.is_authenticated:
        venue = Venue.objects.get(id=id, slug=slug)

        print(venue)

        if request.method == 'POST':
            form = VenueReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.author = request.user

                print(request.user)

                data.venue = venue
                print(data.venue.author)
                if data.venue.author == request.user:
                    messages.error(request, 'You cant give your self a  review clever clogs')
                    return redirect('venue-detail', id, slug)
                else:
                    data.save()

                    messages.success(request, 'Your review has now been posted')
                    return redirect('venue-detail', id, slug)
            else:

                messages.error(request, 'There is a error in your review and it has not been posted')
                return redirect('venue-detail', id, slug)
    else:
        return redirect('sign-in')


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


