from django.conf import settings
from  django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
import stripe

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

    # Handle the event
    if event['type'] == 'payment_intent.created':
        session = event['data']['object']
        print("Payment intent are created")

    if event['type'] == 'payment_intent.processing':
        session = event['data']['object']
        print("Payment intent are processing")

    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        print("Payment intent are successed")

    if event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        print("Payment intent are failed")

    if event['type'] == 'payment_intent.canceled':
        session = event['data']['object']
        print("Payment intent are cancled")
    
    # Passed signature verification
    return HttpResponse(status=200)

