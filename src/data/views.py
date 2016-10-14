# coding=utf-8
from email.mime.text import MIMEText
import smtplib
from rest_framework import views, status
from .serializers import EmailSendSerializer, MessengerSendSerializer, SMSSendSerializer
from rest_framework.response import Response
from twilio.rest import TwilioRestClient
from pymessenger.bot import Bot


class EmailSend(views.APIView):

    @staticmethod
    def post(request):
        serializer = EmailSendSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Create a text/plain message
                msg = MIMEText(serializer.validated_data['message'])

                # me == the sender's email address
                # you == the recipient's email address
                msg['Subject'] = 'Notification'
                msg['From'] = "geral@transafe.pt"
                msg['To'] = serializer.validated_data['email']

                # Send the message via our own SMTP server, but don't include the
                # envelope header.
                s = smtplib.SMTP('localhost')
                s.sendmail("geral@transafe.pt", [serializer.validated_data['email']], msg.as_string())
                s.quit()
            except Exception:
                pass

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
            bot = Bot("EAANBzqOrcZAwBAIumP0PgVDZCQ46fa6pEJR9qIOl41dZBxlzsuEZCBFP0nbMojeNE0WYolQkagA5nizZCg4ZAAH4o0hTDn2fZB1iZAtcfe9Guzif4AXcZCS5ZBITREoxQO0nokT6eLf8F48rWETuQ1QFySSOD0NRQtUGNlOXXQEftvxwZDZD")
            bot.send_text_message("108978599563108", "OLA")

            """
            140064409787860 | 108978599563108

            typical error:
            {"error":{"message":"(#100) No matching user found","type":"OAuthException","code":100,"fbtrace_id":"HwK4\/gmHyzP"}}
            """

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
            account_sid = "AC3698941d227f14fab41f091ce45893f4"
            auth_token = "343dff7352d4775e4e9c32cc5df7afcc"

            client = TwilioRestClient(account_sid, auth_token)

            try:
                message = client.messages.create(body=serializer.validated_data['message'],
                                                 to=serializer.validated_data['number'],  # Replace with your phone number
                                                 from_="+351308805125")  # Replace with your Twilio number
                print(message.sid)
            except Exception:
                pass

            return Response({'status': 'Good request',
                             'message': 'Fake message sent!'},
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad request',
                         'message': 'The data that you send is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)
