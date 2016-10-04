from django.conf.urls import url
from .views import EmailSend, MessengerSend, SMSSend

urlpatterns = [
               url(r'^email/$', EmailSend.as_view(), name="Send email"),
               url(r'^messenger/$', MessengerSend.as_view(), name="Send email to facebook messenger"),
               url(r'^sms/$', SMSSend.as_view(), name="Send SMS"),
]
