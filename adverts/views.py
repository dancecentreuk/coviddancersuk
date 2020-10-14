from django.shortcuts import render, redirect
from .models import Advert, Posting
from .forms import AdvertForm, PostingForm
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from pages.choices import location_choices


def adverts(request):
    adverts = Advert.objects.filter(is_posting=False).filter(is_published=True).order_by('-created')
    paginator = Paginator(adverts, 10)
    page = request.GET.get('page')
    paged_adverts = paginator.get_page(page)
    context = {
        'location_choices':location_choices,
        'adverts':paged_adverts
    }
    return render(request, 'adverts/adverts.html', context)


def advert_detail(request, pk, slug):
    advert = Advert.objects.get(pk=pk, slug=slug)
    context = {
        'advert': advert,

    }
    return render(request, 'adverts/advert_detail.html', context)


def advert_create(request):
    if request.method == 'POST':
        form = AdvertForm(request.POST or None)

        #check if form is valid
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.save()

            # redirect to created post
            return redirect ('advert-detail', data.pk,  data.slug)
    else:
        form = AdvertForm()
    context = {
        'form':form

    }
    return render(request, 'adverts/create_advert.html', context)


def edit_job(request, pk, slug):
    advert = Advert.objects.get(id=pk)
    if advert.author == request.user:
        if request.method == 'POST':
            form = AdvertForm(request.POST or None, instance=advert)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return redirect('advert-detail', data.pk,  data.slug)
        else:
            form = AdvertForm(instance=advert)
        context = {
            'form':form
        }
        return render(request, 'adverts/create_advert.html', context)
    else:
        return redirect('adverts')


def delete_advert(request, pk, slug):
    # get the advert
    advert = Advert.objects.get(id=pk, slug=slug)
    # delete the advert
    advert.delete()
    messages.success(request, ('item has been deleted'))
    return redirect('adverts')


#
# def delete_advert2(request, pk, slug):
#     advert = Advert.objects.get(id=pk, slug=slug)
#     if request.method == 'POST':
#         advert.delete()
#         return redirect('adverts')
#     context = {
#         'advert':advert
#     }
#     return render(request, 'adverts/delete_advert.html', context)



def postings(request):
    postings = Advert.objects.filter(is_posting=True).filter(is_published=True).order_by('date')

    paginator = Paginator(postings, 10)
    page = request.GET.get('page')
    paged_postings = paginator.get_page(page)
    context = {
        'postings': paged_postings,
        'location_choices': location_choices
    }
    return render(request, 'adverts/postings.html', context)


def posting_detail(request, pk, slug):
    posting = Advert.objects.get(pk=pk, slug=slug)
    context = {
        'posting': posting,

    }
    return render(request, 'adverts/posting_detail.html', context)


def posting_create(request):
    if request.method == 'POST':
        form = PostingForm(request.POST or None)

        #check if form is valid
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.is_posting = True
            data.save()

            # redirect to created post
            return redirect('posting-detail', data.pk, data.slug)
    else:
        form = PostingForm()
    context = {
        'form':form

    }
    return render(request, 'adverts/create_posting.html', context)


def edit_posting(request, pk, slug):
    posting = Advert.objects.get(id=pk)
    if request.user == posting.author:
        if request.method == 'POST':
            form = PostingForm(request.POST or None, instance=posting)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return redirect('posting-detail', data.pk,  data.slug)
        else:
            form = PostingForm(instance=posting)
        context = {
            'form':form
        }
        return render(request, 'adverts/create_advert.html', context)
    else:
        return redirect('postings')


def delete_posting(request, pk, slug):
    # get the advert
    posting = Advert.objects.get(id=pk, slug=slug)
    if request.user == posting.author:
        # delete the advert
        posting.delete()
        messages.success(request, ('item has been deleted'))
        return redirect('postings')
    else:
        return redirect('postings')


def search(request):


    queryset_list = Advert.objects.filter(is_posting=False).filter(is_published=True).order_by('-created')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(body__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(location=city)


    context = {

        'adverts': queryset_list,
        'location_choices':location_choices,
        'values': request.GET



    }

    return render(request, 'adverts/search.html', context)


def postings_search(request):


    queryset_list = Advert.objects.filter(is_posting=True).filter(is_published=True).order_by('date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(body__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(location=city)


    context = {

        'postings': queryset_list,
        'location_choices':location_choices,
        'values': request.GET



    }

    return render(request, 'adverts/search_posting.html', context)



