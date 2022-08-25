
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeAPI:

    # Create customer user 
    def create_customer(email):
        return stripe.Customer.create(email=email)
    
    #Create payment method
    def create_payment_method(number, exp_month, exp_year, cvc):
        return stripe.PaymentMethod.create(
                type="card",
                card={
                    "number":  number,
                    "exp_month":exp_month ,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },)

    # Attach Payment method to a Customer
    def attach(stripe_payment, stripe_account):
        return stripe.PaymentMethod.attach(stripe_payment,customer = stripe_account)

    #detach payment method
    def detach(payment_method):
        return stripe.PaymentMethod.detach(payment_method)

    # List payment method of user by customer
    def get_list_payment_method(stripe_account):
        return stripe.Customer.list_payment_methods(stripe_account,type="card")

    #List payment method by Payment Method
    def get_list_payment_method_by_pm(customer):
        return stripe.PaymentMethod.list(customer=customer,type="card")

    # Create payment intent
    def create_payment_intent(amount,currency, payment_method_types, order_id,customer_id = None , user = None):
        if customer_id is not None:
            return stripe.PaymentIntent.create(
                customer = customer_id,
                amount = amount, 
                currency = currency,
                payment_method_types=payment_method_types,
                metadata = {
                    "order_id": order_id,
                    "user_id": user
                })
        return stripe.PaymentIntent.create(
            amount = amount, 
            currency = currency,
            payment_method_types=payment_method_types,
            metadata = {
                "order_id": order_id,
                "user_id": user
            })
    
    # Retrieve paymnent intent
    def retrieve_payment_intent(payment_intent):
        return stripe.PaymentIntent.retrieve(
            payment_intent,
            )

    # Confirm paymnent intent
    def confirm_payment_intent(payment_intent, payment_method):
        return stripe.PaymentIntent.confirm(payment_intent,payment_method= payment_method)

    # setup intent
    def setup_intent(payment_method_types,order_id,user_id = None):
        if user_id is not None:
            return stripe.SetupIntent.create(
                payment_method_types=payment_method_types,
                metadata = {
                    "user_id": user_id,
                    "order_id": order_id
                })
        return stripe.SetupIntent.create(
                payment_method_types=payment_method_types,
                 metadata = {
                    "order_id": order_id
                }) 
    
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
        print(queryset)
        data = stripe.PaymentIntent.search(query = queryset )
        charge_id = data.data[0].charges.data[0].id
        return stripe.Refund.create(
            charge=charge_id,
            metadata = {
                    "order_id": order_id
                }
            )