import getsettings
from django.contrib.auth import get_user_model
User = get_user_model()

from validate_email import validate_email

def process_user_emailvalidate():
    users = User.objects.filter(email_isvalid='N')
    for user in users:
        user.email_isvalid = ['I', 'V'][validate_email(user.useremail,verify=True)]
        user.save()
    User.objects.filter(email_isvalid='I').update(status="B")

process_user_emailvalidate()