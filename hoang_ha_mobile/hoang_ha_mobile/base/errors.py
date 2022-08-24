from rest_framework import response, status

from comments.models import Comment
from orders.models import Order
from variants.models import Variant
from accounts.models import StripeAccount

from base.services.stripe.views import StripeAPI

from django.db.models import Q


def check_valid_item(items):
    if(len(items) < 1): 
        return response.Response(data={"Error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    for item in items:        
        if not (int(item.get('quantity')) > 0): 
            return response.Response(data={"Error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        variant = Variant.objects.filter(id = item.get('variant'), status=True, deleted_by=None)
        if not(variant.exists()): 
            return response.Response(data={"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


def check_valid_comment(parent_id, variant_id):
    comment_instance = Comment.objects.filter(variant = variant_id, id = parent_id)
    if not(comment_instance.exists()):
        return response.Response(data={"detail": "Comment failed,Error: Different variant or comment parent, Can't create new instance"}, status=status.HTTP_400_BAD_REQUEST)


def check_rating_exist(user_id, variant_id):
    rate = Comment.objects.filter(~Q(rating=0), created_by=user_id, variant=variant_id)
    if(rate.exists()):
        return response.Response(data={"detail": "Rating existed, Can't create new instance"}, status=status.HTTP_400_BAD_REQUEST)

#check order error
class OrderCheckError:
    
    # Check order exists
    def check_order_exists(order_id):
        if not Order.objects.filter(id=order_id).exists() :
            return response.Response(data={"message":"Order is not exixts"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if your order has not been paid
    def check_order_paid_yet(order_id):
        order = Order.objects.get(id=order_id)
        if order.paid == False :
            message ={
               "message": "Can't refund, because Your order has not been paid !",
             }
            return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)
    
    #Check if your order has been paid
    def check_order_paid(order_id):
        order = Order.objects.get(id=order_id)
        if order.paid == True :
            message ={
                "message": "Your order has been paid !",
                     }
            return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)
    
    #Check if your order has been refund
    def check_order_refund(order_id):
        order = Order.objects.get(id=order_id)
        if order.refund == True :
            message ={
                    "message": "Can't refund, because Your order has been refund !",
                    }
            return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)
    
    #check payment method of user
    def check_valid_payment_method(user_id,payment_method):
        if StripeAccount.objects.filter(user=user_id).exists():
            stripe_account = StripeAccount.objects.get(user=user_id)
            list_payment_method = StripeAPI.get_list_payment_method_by_pm(stripe_account.stripe_account)
            
            valid = False
            
            for pm in list_payment_method :
    
                if pm.id == payment_method :
                    valid = True
            if valid == False :
                message ={
                    "message": "Can't checkout, because Your payment method is wrong !",
                    }
                return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)