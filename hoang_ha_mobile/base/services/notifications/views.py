from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests
import json

def send_notification(registration_ids, message_title, message_desc):
    fcm_api = settings.REGISTRATIONS
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key='+fcm_api
    }

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title,
        }
    }

    result = requests.post(url,  data=json.dump(payload), headers=headers )


class Firebase(APIView):

    def post(self, request):
        registration  = ""
        mess_title = ""
        mess_body = ""
        send_notification(registration ,message_title=mess_title,message_desc=mess_body)
        return Response({"message": "Sucess"})

