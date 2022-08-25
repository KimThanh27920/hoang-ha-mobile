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

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    

def send_notification_with_firebase(title, body):
    registration  = ["dfWq6Nnw727mdaqlNeVCfl:APA91bGKkO6kNjuTt0IQgFG_LdLguxpjcRPgTo1fmH5ybeRsxtG0F5jZTCKzuCUqnZosTnSX4oAQdN5yhDEMaQsVCpQJeGTM5BbSRSnRqGIvPcgYEu3gycpuJb_qjphkBL6SXaVLEj1B"]
    mess_title = title
    mess_body = body
    send_notification(registration ,message_title=mess_title,message_desc=mess_body)