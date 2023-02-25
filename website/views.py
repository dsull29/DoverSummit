import smtplib
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils.html import format_html
from email.utils import formataddr
from django.contrib import messages
from django.conf import settings

from .forms import ContactForm


def home(request):

    if request.method == "POST":
        return handle_post(request)

    form = ContactForm()
    return render(request, 'website/index.html', {'form': form})


def handle_post(request):
    form = ContactForm(request.POST)

    if form.is_valid():
        subject = "Website Inquiry"
        from_email = formataddr(('Dover Summit', settings.EMAIL_HOST_USER))
        message = format_html('<p>Name: {}</p><p>Email: {}</p><p>Message: {}</p>',
                              form.cleaned_data['name'], form.cleaned_data['email_address'], form.cleaned_data['message'])
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Your email has been sent successfully!')
        except (BadHeaderError, smtplib.SMTPException) as e:
            messages.error(
                request, 'Oops! Something went wrong. Please try again later.')
            return HttpResponse('Invalid header or SMTPException found.')
        return redirect("home")
