from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from  django.contrib import messages
from django.views import View
from validate_email import validate_email
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from accounts.models import User
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)


    def run(self):
        self.email.send(fail_silently=False)

def profile(request):
    if request.user.is_authenticated:
        if request.user.is_candidate:
            return redirect('candidate-profile')
        else:
            if request.user.is_employer:
                return redirect('employer-profile')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    context = {

    }
    return render(request, 'registration/signup.html', context)


def sign_in(request):


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, ' : Welcome ' + user.first_name + ' You are now logged in')
                    return redirect('index')

            else:
                messages.error(request, ' Have you activated your account ps check email ')
                return render(request, 'accounts/login.html', )

        else:
            messages.error(request, 'invalid credentials')
            return render(request, 'accounts/login.html', )

    else:
        return render(request, 'accounts/login.html', )



def logout_user(request):
    logout(request)
    return redirect('sign-in')


class RequestPassword(View):
    def get(self, request):
        return render(request, 'registration/reset-password.html')

    def post(self, request):
        email = request.POST['email']



        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'PS Supply A Valid Email Address')
            return render(request, 'registration/reset-password.html', context)
        else:

            domain = get_current_site(request).domain

            # user = request.objects.filter(email=email)

            user = User.objects.filter(email=email)

            print(user)




            if user.exists():

                uid = urlsafe_base64_encode(force_bytes(user[0].pk))

                email_contents = {
                    'user': user[0],
                    'domain': domain,
                    'uid': uid,
                    'token': PasswordResetTokenGenerator().make_token(user[0])

                }

                link = reverse('reset-password', kwargs={
                    'uidb64':email_contents['uid'], 'token': email_contents['token']})

                reset_url =  'http://'+domain+link

                email_subject = 'Password reset Instructions'
                email_body = 'Hi Please click on the link below to reset your password \n'  + reset_url
                email_address = email
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@dance.com',
                    [email_address]

                )
                EmailThread(email).start()

            messages.success(request, 'We have sent you an email')


        return render(request, 'registration/reset-password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid ps request a  new one')
                return redirect('password-reset-link')


        except Exception as identifier:
            pass
        return render(request, 'registration/set-new-password.html', context)


    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2 :
            messages.error(request, 'Your passwords are not matching')
            return render(request, 'registration/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password to short')
            return render(request, 'registration/set-new-password.html', context)


        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            user.set_password(password)
            user.save()

            messages.success(request, 'Your password has been reset ps login')
            return redirect('sign-in')
        except Exception as identifier:
            messages.info(request, 'something went wrong')
            return render(request, 'registration/set-new-password.html', context)




