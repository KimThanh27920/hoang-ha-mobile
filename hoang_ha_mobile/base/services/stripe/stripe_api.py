
from distutils.log import error
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeAPI:

    # Create customer user 
    def create_customer(email):
        return stripe.Customer.create(email=email)
    
    #Create payment method
    def create_payment_method(number, exp_month, exp_year, cvc):
        try :
            pm = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number":  number,
                    "exp_month":exp_month ,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },)
        except stripe.error.CardError:
               return False
        
        return pm         

    # Attach Payment method to a Customer
    def attach(stripe_payment, stripe_account):
        return stripe.PaymentMethod.attach(stripe_payment,customer = stripe_account)

    #detach payment method
    def detach(payment_method):
        return stripe.PaymentMethod.detach(payment_method)

    # List payment method of user by customer
    def get_list_payment_method(stripe_account):
        list_pm = stripe.Customer.list_payment_methods(stripe_account,type="card")
        data = []
        for pm in list_pm["data"] : 
            if pm["customer"] is not None:
                sub = {
                    "id": pm["id"],
                    "exp_month": pm["card"]["exp_month"],
                    "exp_year" : pm["card"]["exp_year"],
                    "last4": pm["card"]["last4"],
                    "customer": pm["customer"]        
                }
            else :
                sub = {
                    "id": pm["id"],
                    "exp_month": pm["exp_month"],
                    "exp_year" : pm["exp_year"],
                    "last4": pm["last4"],
                    "customer": pm["customer"]        
                }
            
            data.append(sub)

        return data



    #List payment method by Payment Method
    def get_list_payment_method_by_pm(customer):
        return stripe.PaymentMethod.list(customer=customer,type="card")

    # Create payment intent
    def create_payment_intent(amount,currency, payment_method_types, order_id,customer_id = None , user = None):
        
        if user is None:
             payment = stripe.PaymentIntent.create(
               
                amount = amount, 
                currency = currency,
                payment_method_types=payment_method_types,
                metadata = {
                    "order_id": order_id,
                }) 
        else: 
            if customer_id is not None:
                payment = stripe.PaymentIntent.create(
                    customer = customer_id,
                    amount = amount, 
                    currency = currency,
                    payment_method_types=payment_method_types,
                    metadata = {
                        "order_id": order_id,
                        "user_id": user
                    })
            else :
                payment = stripe.PaymentIntent.create(
                    amount = amount, 
                    currency = currency,
                    payment_method_types=payment_method_types,
                    metadata = {
                        "order_id": order_id,
                        "user_id": user
                    })
        data = {
            "id": payment["id"],
            "client_secret": payment["client_secret"],
            "amount": payment["amount"],
            "currency": payment["currency"],
            "payment_method_types": payment["payment_method_types"],
            "status": payment["status"],
            "metadata": payment["metadata"]

        }
        return data
   
    # Retrieve paymnent intent
    def retrieve_payment_intent(payment_intent):
        return stripe.PaymentIntent.retrieve(
            payment_intent,
            )

    # Confirm paymnent intent
    def confirm_payment_intent(payment_intent, payment_method):
        
        try:
            payment = stripe.PaymentIntent.confirm(payment_intent,payment_method= payment_method)
        
            data = {
                "id": payment["id"],
                "client_secret": payment["client_secret"],
                "amount": payment["amount"],
                "currency": payment["currency"],
                "payment_method_types": payment["payment_method_types"],
                "status": payment["status"],
                "metadata": payment["metadata"],
                "amount_received": payment["amount_received"],
                "charges":{
                    "id": payment["charges"]["data"][0]["id"],
                    "amount": payment["charges"]["data"][0]["amount"],
                    "currency": payment["charges"]["data"][0]["currency"],
                    "paid": payment["charges"]["data"][0]["paid"],
                    "status": payment["charges"]["data"][0]["status"],

                }

            }
        except stripe.error.CardError as e :
            
            error = {
                "message": "Can't checkout! Because your card has insufficient funds",
                "status" : False
            }
            return error
        except stripe.error.InvalidRequestError as e:
            error = {
                "message": "The provided PaymentMethod was previously used with a PaymentIntent without Customer attachment, shared with a connected account without Customer attachment, or was detached from a Customer. It may not be used again. To use a PaymentMethod multiple times, you must attach it to a Customer first.",
                "status" : False
            }
            return error
        except stripe.error.APIConnectionError as e:
            error = {
                "message": "Network communication with Stripe failed",
                "status" : False
            }
            return error
        except Exception as e:
            error = {
                "message": "Somethings was wrong! "+str(e),
                "status" : False
            }
            return error  
        
        return data


    # setup intent
    def setup_intent(payment_method_types,user_id = None):
        if user_id is not None:
            return stripe.SetupIntent.create(
                payment_method_types=payment_method_types,
                metadata = {
                    "user_id": user_id,
                })
        return stripe.SetupIntent.create(
                payment_method_types=payment_method_types,) 
    
    #retrieve set up intent
    def retrieve_setup_intent(setup_intent):
        return stripe.SetupIntent.retrieve(
            setup_intent,
            )

    #confirm setup intent
    def confirm_setup_intent(setup_intent_id, payment_method):
        return stripe.SetupIntent.confirm(
            setup_intent_id,
            payment_method = payment_method
        )


    # Refund 
    def refund(order_id):
        queryset = "metadata['order_id']:"+"'"+str(order_id)+"'"
        data = stripe.PaymentIntent.search(query = queryset )
        charge_id = data.data[0].charges.data[0].id
        try:
            refund = stripe.Refund.create(
                charge=charge_id,
                metadata = {
                        "order_id": order_id
                    }
                )
        except Exception as e:
            print(e)
            return False
        
        data = {
            "id": refund["id"],
            "amount": refund["amount"],
            "currency": refund["currency"],
            "charges": refund["charge"],
            "status": refund["status"],
            "metadata": refund["metadata"],

        }
        return data