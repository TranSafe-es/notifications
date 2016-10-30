# coding=utf-8
import threading
from email.mime.text import MIMEText
import smtplib
from rest_framework import views, status
from .serializers import EmailSendSerializer, MessengerSendSerializer, SMSSendSerializer
from rest_framework.response import Response
from twilio.rest import TwilioRestClient
import requests
import thread


def send_mail(message, email):
    try:
        # Create a text/plain message
        msg = MIMEText(message)

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'Notification'
        msg['From'] = "transafe@rafaelferreira.pt"
        msg['To'] = email

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP("smtp.zoho.com", 465)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("transafe@rafaelferreira.pt", "transafe2016")
        s.sendmail("transafe@rafaelferreira.pt", [email], msg.as_string())
        s.quit()
    except Exception:
        pass


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
            process_thread = threading.Thread(target=send_mail, args=[serializer.validated_data['message'],
                                                                      serializer.validated_data['email']])
            process_thread.daemon = True
            process_thread.start()

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
            process_thread = threading.Thread(target=send_messenger, args=[serializer.validated_data['message'],
                                                                           serializer.validated_data['phone_number']])
            process_thread.daemon = True
            process_thread.start()

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
            process_thread = threading.Thread(target=send_sms, args=[serializer.validated_data['message'],
                                                                     serializer.validated_data['phone_number']])
            process_thread.daemon = True
            process_thread.start()

            return Response({'status': 'Good request',
                             'message': 'Fake message sent!'},
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad request',
                         'message': 'The data that you send is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)
