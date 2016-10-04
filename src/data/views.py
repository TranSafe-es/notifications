# coding=utf-8
from email.mime.text import MIMEText
import smtplib
from rest_framework import views, status
from .serializers import EmailSendSerializer, MessengerSendSerializer, SMSSendSerializer
from rest_framework.response import Response
from twilio.rest import TwilioRestClient
import requests


class EmailSend(views.APIView):

    @staticmethod
    def post(request):
        serializer = EmailSendSerializer(data=request.data)

        if serializer.is_valid():
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
            access_token = "EAANBzqOrcZAwBAHI674rcAIB2Eg1u7cZCJo31SwoUJXfRZBUMpp9I6ZC5GGIG1kCh6UrrdikxtwjZBt0ySUyZAS2aCSezwqKS54JFXtmmXiVj88RkXU231flecsXRWK5K2nvp655HkBh9iRfVzvcM1icnh4h2mrF5tZCcRVYgO4BAZDZD"
            r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token, data={
                                "recipient": {
                                    "id": serializer.validated_data['profile_id']
                                },
                                "message":{
                                    "text": serializer.validated_data['message']
                                }
                              })

            """
            typical error:
            {"error":{"message":"(#100) No matching user found","type":"OAuthException","code":100,"fbtrace_id":"HwK4\/gmHyzP"}}
            """

            print r

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
