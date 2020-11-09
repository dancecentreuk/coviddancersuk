from django.shortcuts import render, redirect
from .models import WeeklyDanceClass, ClassImage, DanceClassReview
from pages.choices import dance_styles, location_choices, level, age_choices, day
from .forms import DanceClassForm, DancePhotoForm, DanceClassReviewForm
from django.urls import reverse
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import PageNotAnInteger, Paginator, Page, EmptyPage


# Create your views here.


def dance_classes(request):
    dance_classes = WeeklyDanceClass.objects.all().filter(is_allowed=True).filter(is_published=True).order_by('-created')

    paginator = Paginator(dance_classes, 10)
    page = request.GET.get('page')
    paged_dance_classes = paginator.get_page(page)

    dance_classes_sunday = dance_classes.filter(day='Sunday')
    dance_classes_monday = dance_classes.filter(day='Monday')
    dance_classes_tuesday = dance_classes.filter(day='Tuesday')
    dance_classes_wednesday = dance_classes.filter(day='Wednesday')
    dance_classes_thursday = dance_classes.filter(day='Thursday')
    dance_classes_friday= dance_classes.filter(day='Friday')
    dance_classes_saturday = dance_classes.filter(day='Saturday')


    context = {
        'day':day,
        'level':level,
        'age_choices': age_choices,
        'location_choices':location_choices,
        'dance_classes': paged_dance_classes,
        'dance_classes_sunday':dance_classes_sunday,
        'dance_classes_monday':dance_classes_monday,
        'dance_classes_tuesday':dance_classes_tuesday,
        'dance_classes_wednesday': dance_classes_wednesday,
        'dance_classes_thursday': dance_classes_thursday,
        'dance_classes_friday': dance_classes_friday,
        'dance_classes_saturday': dance_classes_saturday,
        'dance_styles': dance_styles
    }
    return render(request, 'dance_classes/dance_classes.html', context)


def add_dance_class(request):
    if request.method == 'POST':
        form = DanceClassForm(request.POST, request.FILES or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.author  = request.user.candidate
            data.is_published = True
            data.save()
            return redirect('dance-class-detail', data.id)
    else:
        form = DanceClassForm()
    context = {
        'form':form

    }
    return render(request, 'dance_classes/add_dance_class.html', context)




def edit_dance_class(request, id):



    if request.user.is_authenticated:
        dance_class = WeeklyDanceClass.objects.get(id=id)
        if request.user == dance_class.author.user:
            if request.method == 'POST':
                form = DanceClassForm(request.POST, request.FILES or None, instance=dance_class)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('dance-class-detail', dance_class.id)


            else:
                form = DanceClassForm(instance=dance_class)
            context = {
                'form': form
            }
            return render(request, 'dance_classes/add_dance_class.html', context)
        else:

            messages.error(request, ('you are not the creator of this dance class'))
            return redirect('dance-class-detail', dance_class.id)
    else:
        messages.error(request, ('you need to login to edit class details'))
        return redirect('sign-in')




# def edit_dance_class(request, id):
#
#     dance_class = WeeklyDanceClass.objects.get(id=id)
#
#     if request.method == 'POST':
#         form = DanceClassForm(request.POST, request.FILES or None, instance=dance_class)
#
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.save()
#             return redirect('dance-class-detail', dance_class.id)
#
#
#     else:
#         form = DanceClassForm(instance=dance_class)
#     context = {
#         'form':form
#     }
#     return render(request, 'dance_classes/add_dance_class.html', context)


def dance_class_detail(request, id):

    dance_class = WeeklyDanceClass.objects.get(id=id)
    dance_photos = ClassImage.objects.filter(dance_class=id)
    reviews = DanceClassReview.objects.filter(danceClass=id).order_by('-created')
    average_reviews = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_reviews is not None:
        average_reviews = round(average_reviews, 1)



    context = {

        'dance_class':dance_class,
        'dance_photos': dance_photos,
        'reviews': reviews,
        'average_reviews': average_reviews


    }
    return render(request, 'dance_classes/dance_class_detail.html', context)


def delete_dance_class(request, pk):

    dance_class = WeeklyDanceClass.objects.get(id=pk)
    if request.user == dance_class.author.user:
        dance_class.delete()
        messages.success(request, ('item has been deleted'))
        return redirect('dance-classes')
    else:
        messages.error(request, ('this has not been deleted'))
        return redirect('dance-class-detail', dance_class.id)




def dance_classes_search(request):


    queryset_list = WeeklyDanceClass.objects.all().filter(is_allowed=True).filter(is_published=True).order_by('-created')


    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(about__icontains=keywords)

    if 'dance_style' in request.GET:
        dance_style_choice = request.GET['dance_style']
        if dance_style_choice:
            queryset_list = queryset_list.filter(dance_style_choice=dance_style_choice)


    if 'class_level' in request.GET:
        class_level = request.GET['class_level']
        if class_level:
            queryset_list = queryset_list.filter(level=class_level)


    if 'search_day' in request.GET:
        search_day = request.GET['search_day']
        if search_day:
            queryset_list = queryset_list.filter(day=search_day)

    if 'age' in request.GET:
        age = request.GET['age']
        if age:
            queryset_list = queryset_list.filter(age_group=age)


    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(location=city)



    dance_classes_sunday = queryset_list.filter(day='Sunday')
    dance_classes_monday = queryset_list.filter(day='Monday')
    dance_classes_tuesday = queryset_list.filter(day='Tuesday')
    dance_classes_wednesday = queryset_list.filter(day='Wednesday')
    dance_classes_thursday = queryset_list.filter(day='Thursday')
    dance_classes_friday = queryset_list.filter(day='Friday')
    dance_classes_saturday = queryset_list.filter(day='Saturday')

    context = {


        'age_choices': age_choices,
        'dance_classes': queryset_list,
        'location_choices':location_choices,
        'dance_styles': dance_styles,
        'level': level,
        'day':day,
        'values': request.GET,

        'dance_classes_sunday': dance_classes_sunday,
        'dance_classes_monday':dance_classes_monday,
        'dance_classes_tuesday': dance_classes_tuesday,
        'dance_classes_wednesday': dance_classes_wednesday,
        'dance_classes_thursday': dance_classes_thursday,
        'dance_classes_friday': dance_classes_friday,
        'dance_classes_saturday': dance_classes_saturday,




    }

    return render(request, 'dance_classes/search_dance_classes.html', context)





def dance_class_photo(request):

    if request.method == 'POST':
        form = DancePhotoForm(request.POST, request.FILES or None)

        if form.is_valid():
            data=form.save(commit=False)
            data.owner = request.user.candidate
            data.save()
            return redirect('candidate-profile')

    form = DancePhotoForm(request.POST or None)

    context = {
        'form': form
    }

    return render(request, 'accounts/add-photo.html', context)


def add_dance_class_review(request, id):
    if request.user.is_authenticated:
        dance_class = WeeklyDanceClass.objects.get(id=id)

        print(dance_class)

        if request.method == 'POST':
            form = DanceClassReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.author = request.user

                print(request.user)

                data.danceClass = dance_class
                print(data.danceClass.author.user)
                if data.danceClass.author.user == request.user:
                    messages.error(request, 'You cant give your self a  review clever clogs')
                    return redirect('dance-class-detail', id)
                else:
                    data.save()

                    messages.success(request, 'Your review has now been posted')
                    return redirect('dance-class-detail', id)
            else:

                messages.error(request, 'There is a error in your review and it has not been posted')
                return redirect('dance-class-detail', id)
    else:
        return redirect('sign-in')