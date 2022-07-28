from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib import messages
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import get_template
# from django.template import Context
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_text
# from django.contrib.auth.models import User
# from django.db import IntegrityError
# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from .tokens import account_activation_token
# from django.template.loader import render_to_string

def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        return redirect('dashboard')


def signup(request):
 
    signupForm = RegistrationForm()
    if request.method == 'POST':
        signupForm = RegistrationForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            # --------------------------------------------------------------------------------------------
            # html_body = get_template('registration/registration.html')
            # username=request.get['username']
            # email=request.get['email']
            # d = { 'username': username }
            # subject, from_email, to = 'welcome', 'sharjil.israr@gmail.com', email            
            # html_content = html_body.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            # --------------------------------------------------------------------------------------------
            messages.success(request,'Email sent for validation..')
            return redirect('login')
    return render(request,'registration/signup.html',{'signupForm' : signupForm})       


# def activation_sent_view(request):
#     return render(request, 'activation_sent.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.profile.signup_confirmation = True
#         user.save()
#         login(request, user)
#         return redirect('home')
#     else:
#         return render(request, 'registration/activation_fail.html')