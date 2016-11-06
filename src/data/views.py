# coding=utf-8
import threading
from email.mime.text import MIMEText
import smtplib
from rest_framework import views, status
from .serializers import EmailSendSerializer, MessengerSendSerializer, SMSSendSerializer
from rest_framework.response import Response
from twilio.rest import TwilioRestClient
import requests
from celery import shared_task


@shared_task
def send_mail(message, email):
    try:

        # Define to/from
        sender = 'transafe@rafaelferreira.pt'
        recipient = email

        # Create message
        msg = MIMEText(message)
        msg['Subject'] = "Notification"
        msg['From'] = sender
        msg['To'] = recipient

        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

        # Perform operations via server
        server.login("transafe@rafaelferreira.pt", "transafe2016")
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
    except Exception:
        pass


@shared_task
def send_messenger(phone_number, message):
    access_token = "EAANBzqOrcZAwBANugFBOpt8hZAdno4l2N3bJY9Y5LYd9156NP1ZAm09rnKZByWpVrPzur9pEGoOJjMEuvZCqhOCv4m07wNGA18ZBve0V94r8XLCWfSvGIiKi91r24YbruvPHX5ZB8GtnZBFCzwrXYMqEaaNwfRSNV2WgksBFD0it0AZDZD"
    r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token, json={
        "recipient": {
            "phone_number": phone_number
        },
        "message": {
            "text": message
        }
    })


@shared_task
def send_sms(phone_number, message):
    account_sid = "AC3698941d227f14fab41f091ce45893f4"
    auth_token = "343dff7352d4775e4e9c32cc5df7afcc"

    client = TwilioRestClient(account_sid, auth_token)

    try:
        message = client.messages.create(body=message,
                                         to=phone_number,  # Replace with your phone number
                                         from_="+351308805125")  # Replace with your Twilio number
        print(message.sid)
    except Exception:
        pass


class EmailSend(views.APIView):

    @staticmethod
    def post(request):
        serializer = EmailSendSerializer(data=request.data)

        if serializer.is_valid():
            send_mail.apply_async(args=[serializer.validated_data['message'],
                                        serializer.validated_data['email']])

            return Response({'status': 'Good request',
                             'message': 'Fake message sent!'},
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad request',
                         'message': 'The data that you send is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)


class MessengerSend(views.APIView):

    @staticmethod
    def post(request):
        serializer = MessengerSendSerializer(data=request.data)

        if serializer.is_valid():
            send_messenger.apply_async(args=[serializer.validated_data['phone_number'],
                                             serializer.validated_data['message']])

            return Response({'status': 'Good request',
                             'message': 'Fake message sent!'},
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad request',
                         'message': 'The data that you send is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)


class SMSSend(views.APIView):

    @staticmethod
    def post(request):
        serializer = SMSSendSerializer(data=request.data)

        if serializer.is_valid():
            send_sms.apply_async(args=[serializer.validated_data['phone_number'],
                                       serializer.validated_data['message']])

            return Response({'status': 'Good request',
                             'message': 'Fake message sent!'},
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad request',
                         'message': 'The data that you send is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)
