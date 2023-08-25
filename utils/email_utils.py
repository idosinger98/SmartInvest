import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from django.contrib.auth.models import User
from dotenv import load_dotenv


load_dotenv()


def connectedApiAndSendEmail(subject_str, content, user=None):
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('MAIL_KEY')
    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    if user is None:
        user = User.objects.filter(username='Manager')[0]

    sender = {"name": 'Smart Invest', "email": 'smartinvest850@gmail.com'}
    to = [{"email": user.email, "name": 'Daniell'}]
    headers = {"Some-Custom-Name": "unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=content,
                                                   sender=sender, subject=subject_str)
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException:
        return False
