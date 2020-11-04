from django.shortcuts import render, redirect
from .models import WeeklyDanceClass
from pages.choices import dance_styles, location_choices, level, age_choices, day
from .forms import DanceClassForm

# Create your views here.


def dance_classes(request):
    dance_classes = WeeklyDanceClass.objects.all().filter(is_allowed=True).filter(is_published=True)
    dance_classes_sunday = dance_classes.filter(day='Sunday')
    dance_classes_monday = dance_classes.filter(day='Monday')
    dance_classes_tuesday = dance_classes.filter(day='Tuesday')
    dance_classes_wednesday = dance_classes.filter(day='Wednesday')
    dance_classes_thursday = dance_classes.filter(day='Thursday')
    dance_classes_friday= dance_classes.filter(day='Friday')
    dance_classes_saturday = dance_classes.filter(day='Sarturday')

    context = {
        'day':day,
        'level':level,
        'age_choices': age_choices,
        'location_choices':location_choices,
        'dance_classes': dance_classes,
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
            return redirect('dance-classes')
    else:
        form = DanceClassForm()
    context = {
        'form':form

    }
    return render(request, 'dance_classes/add_dance_class.html', context)


def edit_dance_class(request, id):

    dance_class = WeeklyDanceClass.objects.get(id=id)

    if request.method == 'POST':
        form = DanceClassForm(request.POST or None, instance=dance_class)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('dance-classes')

    else:
        form = DanceClassForm(instance=dance_class)
    context = {
        'form':form
    }
    return render(request, 'dance_classes/add_dance_class.html', context)


def dance_class_detail(request, id):

    dance_class = WeeklyDanceClass.objects.get(id=id)



    context = {

        'dance_class':dance_class

    }
    return render(request, 'dance_classes/dance_class_detail.html', context)
