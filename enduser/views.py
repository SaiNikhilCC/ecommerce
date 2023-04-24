from jsonschema import ValidationError
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from ecommerce.customauth import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main import models
from . import enduser_serializers
from rest_framework.filters import SearchFilter
from rest_framework import generics
from sadmins import admin_serializer
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import random


# FAST2SMS API To Send OTP Code
url = "https://www.fast2sms.com/dev/bulkV2"

def sendsms(num, phone):
    payload = f"sender_id=FTWSMS&message=To Verify Your Mobile Number with Ecommerce is {num} &route=v3&numbers={phone}"
    print(payload)
    headers = {
        'authorization': "ulBGWHeNb4qJ9KmyA1fip0RdPYh6kXjwEscTSQ3ODFvC2rgnIZezvgnxpTBcjmlJZQAkY7LKVSHGMU4d",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = "sent"
    response = requests.request("POST", url, data=payload, headers=headers)
    return True
# End of FAST2SMS API


# USER REGISTRATION AND REQUESTS FOR OTP
class RegisterUser(APIView):
    try:
        def post(self, request):
            if models.EndUser.objects.filter(phone=request.data['phone']):
                return Response({
                    'status':400,
                    'errors':'user already existswih this number try loging in'
                })
            serializer = enduser_serializers.EndUserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'some error occurred'})
            serializer.save()
            otp = serializer.data['otp']
            phone = serializer.data['phone']

            # sendsms(otp,phone,device_id)
            print("OTP to Verify Your Number is : ",
                  otp, " -----> sent to : ", phone)
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'success'
            })
    except Exception as e:
        raise ValidationError('somthing went wrong')

# Resend OTP For User
class ResendOTP(APIView):
    def post(self,request):
        if models.EndUser.objects.filter(phone=request.data['phone']):
            user = models.EndUser.objects.get(phone=request.data['phone'])
            user.otp = random.randint(10000,99999)
            user.save()
            print(user.otp)
            sendsms(user.otp,user.phone)
            return Response({
                'status':200,
                'data':'OTP Sent To Your Registered Mobile Number'
            })

# USER ENTERS OTP AND GETS VERIFIED BASED ON HIS UUID AND OTP
class VerifyOtp(APIView):
    try:
        def post(self, request):
            if models.EndUser.objects.filter(uid=request.data["uid"], otp=request.data["otp"]):
                user = models.EndUser.objects.get(uid=request.data['uid'])
                user.is_verified = True
                user.otp = ""
                user.save()
                refresh = AccessToken.for_user(user)
                updated_user = models.EndUser.objects.filter(uid=request.data["uid"])
                serializer = enduser_serializers.EndUserSerializer(updated_user, many=True)
                response = Response({
                    'status': 200,
                    'data': serializer.data,
                    'access': str(refresh),
                    'message': 'success'
                })
                response.content_type = "application/json"
                return response
            else:
                return Response({
                    'status': 400,
                    'message': 'incorrect otp'
                })
    except Exception as e:
        raise ValidationError('something went wrong')


# Login API For End user
class Login(APIView):
    def post(self,request):
        if models.EndUser.objects.filter(phone=request.data['phone']):
            user = models.EndUser.objects.get(phone=request.data['phone'])
            user.otp = random.randint(10000,99999)
            user.save()
            sendsms(user.otp,user)
            user_data = models.EndUser.objects.filter(phone=request.data['phone'])
            user_data_serializer = enduser_serializers.EndUserSerializer(user_data,many=True)
            return Response({
                'status': 200,
                'data':user_data_serializer.data,
                'message': 'OTP is Sent To Registered Phone Number'
            })
        else:
            return Response({
                'status': 200,
                'message': 'User Not Found Register Now'
            })

# User Profile
def UserProfile(request,user_id):
    user= models.EndUser.objects.get(pk=user_id)
    serialized_data = enduser_serializers.EndUserSerializer(user).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': UserProfile,
        'request': request,
    }
    return response

# Edit User Profile
class EditUserProfile(APIView):
    def put(self, request,user_id):
        try:
            obj = models.EndUser.objects.get(pk=user_id)
        except models.EndUser.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = enduser_serializers.EndUserSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Profile Updated Succesfully"
            })
        return Response({
            "status":400,
            "errors":serializer.errors,
            "message":"Something Went Wrong"
            })
#Endusers List

class UsersList(APIView):
    def get(self,request):
        users=models.EndUser.objects.all()
        serializer=enduser_serializers.EndUserSerializer(users,many=True)
        return Response({
            'status':200,
            'data':serializer.data,
            'message':'Users List fetched Successfully'
        })

#############################################################   User Cart Details   #####################################################################
# User Add To Cart 
class AddToCart(APIView):
    def post(self,request):
        serializer = enduser_serializers.CartItemsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'errors': serializer.data,
                'message': 'Item added To Cart Succesfully'
            })

# Users Cart List 
class UsersCart(APIView):
    def get(self,request,user_id):
        user_cart = models.CartItems.objects.filter(user_id = user_id)
        user_cart_serializer = enduser_serializers.CartItemsSerializer(user_cart, many=True)
        return Response({
            'status': 200,
            'data': user_cart_serializer.data,
            'message': 'Users Cart Items Fetched Succesfully'
        })

#############################################################   Products   #####################################################################
# All Products List Without Token Authenticatio
class AllProducts(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        products = models.Product.objects.all()
        serializer = admin_serializer.ProductSerializerWithImages(products,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'All Products Fetched Succesfully'
        })

# Particular Product Details Without Token Authentication
def ParticularProductDetails(request,product_id):
    product= models.Product.objects.get(pk=product_id)
    serialized_data = admin_serializer.ProductSerializerWithImages(product).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ParticularProductDetails,
        'request': request,
    }
    return response

# Search Product
class SearchProduct(generics.ListAPIView):
    queryset = models.Product.objects.all()
    # serializer_class = admin_serializer.ProductSerializer
    serializer_class = admin_serializer.ProductSerializerWithImages
    filter_backends = [SearchFilter]
    search_fields = ['description','product_title']

#############################################################   Orders   #####################################################################

# Placing An Order By End User
class CreateOrders(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        order_serializer = enduser_serializers.OrdersSerializer(data= request.data)
        if not order_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': order_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            order_serializer.save()
            return Response({
                'status': 403,
                'data': order_serializer.data,
                'message': 'Order Placed Succesfully'
            })


# Order Cancel Request API by End User
class RequestOrderCancellation(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request,order_id):
        order = models.Orders.objects.get(pk = order_id)
        if order.order_status != "Requested for Cancellation":
            order.order_status = "Requested for Cancellation"
            order.save()
            updated_order_details = models.Orders.objects.filter(id = order_id)
            updated_order_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
            return Response({
                'status': 200,
                'data': updated_order_serializer.data,
                'message': 'Cancel Request Sent Succesfully'
            })
        else:
            updated_order_details = models.Orders.objects.filter(id = order_id)
            updated_order_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
            return Response({
                'status': 200,
                'data': updated_order_serializer.data,
                'message': 'Cancel Request Already Sent'
            })


# Order Details
class OrderDetails(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request,order_id):
        order_details = models.Orders.objects.filter(id = order_id)
        order_details_serializer = enduser_serializers.OrdersSerializer(order_details,many=True)
        return Response({
            'status': 200,
            'data': order_details_serializer.data,
            'message': 'Order Details Fetched Succesfully'
        })

# Orders History
class OrdersHistory(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request,user_id):
        particular_users_orders = models.Orders.objects.filter(user_id = user_id)
        users_orders_serializer = enduser_serializers.OrdersSerializer(particular_users_orders,many=True)
        return Response({
            'status': 200,
            'data': users_orders_serializer.data,
            'message': 'Order History Fetched Succesfully'
        })


#############################################################   User Wishlist   #####################################################################

# Add Product To Wishlist
class AddToWishlist(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        whislist_serializer = enduser_serializers.WishlistSerializer(data= request.data)
        if not whislist_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': whislist_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            whislist_serializer.save()
            return Response({
                'status': 200,
                'data': whislist_serializer.data,
                'message': 'Item Added To Whishlist'
            })

# Particular Users Wishlist
class UsersWishList(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request,user_id):
        wishlist= models.Wishlist.objects.get(user=user_id)
        serialized_data = enduser_serializers.WishlistDetailedSerializer(wishlist)
        return Response({
            'status':200,
            'data':serialized_data.data,
            'message':'Users Wishlist Fetched'
        })


# Remove From Wishlist 
class RemoveFromWishlist(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,wishlist_id):
        if models.Wishlist.objects.filter(id = wishlist_id):
            wishlist = models.Wishlist.objects.get(pk = wishlist_id)
            wishlist.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Item Removed From Whishlist Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'Item Not Found In Wishlist'
            })
        
#############################################################   User Reviews   #####################################################################

# Post A Review
class PostReview(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        review_serializer = enduser_serializers.ReviewSerializer(data = request.data)
        if not review_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': review_serializer.errors,
                'message': 'Some Error Occurred'
            })
        else:
            review_serializer.save()
            return Response({
                'status': 200,
                'data': review_serializer.data,
                'message': 'Review Posted Succesfully'
            })

# Particular Products All Reviews
class ParticularProductReviews(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request,product_id):
        reviews= models.Product.objects.get(pk=product_id)
        serialized_data = admin_serializer.ProductSerializerWithImages(reviews)
        return Response({
            'status': 200,
            'data': serialized_data.data,
            'message': 'Review Fetched Succesfully'
        })



# Edit A Particular Review
class DeleteReview(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,review_id):
        if models.Reviews.objects.filter(id = review_id):
            review = models.Reviews.objects.get(pk = review_id)
            review.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Review Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'Review With This Already Deleted'
            })

# Replies Received To a Particular Review
class ReceivedReviewsToAParticularReview(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request,review_id):
        reviews= models.ReplyReviews.objects.get(pk=review_id)
        serialized_data = admin_serializer.ReplyToReviewSerializer(reviews)
        return Response({
            'status': 200,
            'data': serialized_data.data,
            'message': 'Review Replies Fetched Succesfully'
        })








