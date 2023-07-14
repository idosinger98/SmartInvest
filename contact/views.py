from django.contrib import messages
from contact.forms import ContactForm
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.http import HttpResponse
import os
from dotenv import load_dotenv
from email_utils import connectedApiAndSendEmail


load_dotenv()


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = f"Name: {body['name']}<br><br>Email: {body['email']}<br><br>Message: {body['message']}"
            connectedApiAndSendEmail(subject_str=form.cleaned_data['subject'], content=message)

            return HttpResponse()

    return HttpResponse()
