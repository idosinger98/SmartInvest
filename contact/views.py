from django.shortcuts import render, redirect
from django.contrib import messages
from contact.forms import ContactForm
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.http import HttpResponse
import os
from dotenv import load_dotenv


load_dotenv()


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = f"Name: {body['name']}<br><br>Email: {body['email']}<br><br>Message: {body['message']}"
            # Configure API key authorization: api-key
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key[
                'api-key'] = os.environ.get('MAIL_KEY')

            # create an instance of the API class
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            html_content = message
            sender = {"name": 'Smart Invest', "email": 'smartinvest850@gmail.com'}
            to = [{"email": 'smartinvest850@gmail.com', "name": 'Daniell'}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content,
                                                           sender=sender, subject=subject)
            try:
                api_instance.send_transac_email(send_smtp_email)
                messages.success(request, "Email send successfully")
            except ApiException:
                return HttpResponse('Invalid header found')

            return HttpResponse()

    return HttpResponse()
