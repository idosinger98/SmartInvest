import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from django.contrib.auth.models import User


def connectedApiAndSendEmail(subject_str, content, user=None):
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('MAIL_KEY')

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    subject = subject_str
    html_content = content
    sender = {"name": 'Smart Invest', "email": 'smartinvest850@gmail.com'}
    if user is not None:
        to = [{"email": user.email, "name": 'Daniell'}]
    else:
        to = [{"email": 'smartinvest850@gmail.com', "name": 'Daniell'}]
    headers = {"Some-Custom-Name": "unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content,
                                                   sender=sender, subject=subject)
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException:
        return False
