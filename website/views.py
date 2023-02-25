from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings


def home(request):

    if request.method == "POST":
        return handle_post(request)

    form = ContactForm()
    return render(request, 'website/index.html', {'form': form})


def handle_post(request):
    form = ContactForm(request.POST)

    if form.is_valid():
        subject = "Website Inquiry"
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email_address'],
            'message': form.cleaned_data['message'],
        }
        message = "\n".join(body.values())

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      settings.EMAIL_LIST)
            messages.success(request, 'Your email has been sent successfully!')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect("home")
