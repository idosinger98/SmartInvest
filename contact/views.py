from contact.forms import ContactForm
from django.http import HttpResponse
from dotenv import load_dotenv
from utils.email_utils import connectedApiAndSendEmail
from django.contrib import messages


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
            messages.success(request, 'Email sent successfully')  # Add success message
            return HttpResponse()

    return HttpResponse()
