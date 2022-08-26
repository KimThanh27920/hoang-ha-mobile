import firebase_admin
import requests
import json
from fcm_django.models import FCMDevice
from django.conf import settings
from firebase_admin import messaging

from accounts.models import CustomUser



#Cloud Messaging API (old version)
class Message:
    def send_notification(self,registration_ids, message_title, message_desc):
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
        

    def send_notification_with_firebase(self,title, body):
        registration  = ["dfWq6Nnw727mdaqlNeVCfl:APA91bGKkO6kNjuTt0IQgFG_LdLguxpjcRPgTo1fmH5ybeRsxtG0F5jZTCKzuCUqnZosTnSX4oAQdN5yhDEMaQsVCpQJeGTM5BbSRSnRqGIvPcgYEu3gycpuJb_qjphkBL6SXaVLEj1B"]
        mess_title = title
        mess_body = body
        self.send_notification(registration ,message_title=mess_title,message_desc=mess_body)


#Firebase Cloud Messaging API (V1)
class FirebaseCloudMessaging: 

    def sendPush(self,title, msg, registration_token, dataObject=None):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=msg
            ),
            data=dataObject,
            tokens=registration_token
        )
        messaging.send_multicast(message)
    
    def fcm_send(self,token_device, title, body):
        # get device token of admin account
        registration = [token_device]
        # call function sendPush to push notification 
        self.sendPush(registration, title, body)


#send notifications with FCM Django
class FCM:
    def send_message_to( title, body):
        admin_account  = CustomUser.objects.filter(is_superuser = True) 
        # devices = []
        
        for acc in admin_account :
            device = FCMDevice.objects.filter(user= acc.id)
            # devices = devices.append(device)

            message = messaging.Message (
                data={
                    "title" : title,
                    "body" : body,            
                }
            )
            device.send_message(message)


        
