from django.shortcuts import render


def register(request):
    context = {

    }
    return render(request, 'registration/signup.html', context)

