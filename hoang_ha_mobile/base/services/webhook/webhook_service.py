from django.conf import settings
from  django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
import stripe
from datetime import datetime
from django.utils import timezone

from transactions.views import create_transaction

# @csrf_exempt
@api_view(['POST'])
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    session = None
    # Handle the event
    if event['type'] == 'charge.succeeded':
        session = event['data']['object']
        type = "charge"

    if event['type'] == 'charge.refunded':
        session = event['data']['object']
        type = "refund"
    
    #add data into database
    if session is not None:
        print(session)
        amount = session['amount']
        if amount > 0 :
            transaction = {
                "datetime": timezone.now()  ,
                "type": type, 
                "amount":amount,
                "currency": session['currency'],
                "description": session['description'],
                "order": session['metadata']['order_id'],
                "payment_intent": session['payment_intent'], 
                "customer": session['metadata']['user_id'],
                "last4": session['payment_method_details']['card']['last4']
            }
            print(session['object'])
            create_transaction(data=transaction)
      
    # Passed signature verification
    return HttpResponse(status=200)

