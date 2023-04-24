from jsonschema import ValidationError
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from ecommerce.customauth import CustomAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from main import models
from . import admin_serializer
from rest_framework import generics
from rest_framework import status
from rest_framework.renderers import JSONRenderer

#############################################################   States   #####################################################################
# All States List Create API View
class StatesList(generics.ListCreateAPIView):
    queryset = models.State.objects.all()
    serializer_class = admin_serializer.StateSerializer

#############################################################   Districts   #####################################################################
# All Districts List API View
class CreateDistrictsList(generics.ListCreateAPIView):
    serializer_class = admin_serializer.CreateDistrictSerializer
    queryset = models.Disrtict.objects.all()

class DistrictsList(generics.ListCreateAPIView):
    serializer_class = admin_serializer.DistrictSerializer
    def get_queryset(self):
        state_id = self.kwargs['state_id']
        state = models.State.objects.get(pk=state_id)
        return (models.Disrtict.objects.filter(state=state))

class AllDistrictsDetailedView(generics.ListAPIView):
    serializer_class = admin_serializer.AllDistrictsDetailedSerializer
    queryset = models.Disrtict.objects.all()

#############################################################   Mandals   #####################################################################
# All Mandals List API View
class CreateMandals(generics.ListCreateAPIView):
    serializer_class = admin_serializer.CreateMandalSerializer
    queryset = models.Mandal.objects.all()

class AllMandalsDetailedView(generics.ListAPIView):
    serializer_class = admin_serializer.AllMandalsDetailSerializer
    queryset = models.Mandal.objects.all()

class MandalsList(generics.ListCreateAPIView):
    serializer_class = admin_serializer.MAndalSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        district = models.Disrtict.objects.get(pk=district_id)
        return (models.Mandal.objects.filter(district=district))

#############################################################   Super Admin   #####################################################################
# Super Admin Login View
class SuperAdminLoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        superadmin = models.SuperAdminAcc.objects.filter(username=username, password=password)
        serializer = admin_serializer.SuperAdminAccSerializer(superadmin, many=True)
        admin_acc = models.SuperAdminAcc.objects.get(username=username)
        access_token = AccessToken.for_user(admin_acc)
        if superadmin:
            return Response({
                "status": 200,
                "bool": True,
                "data": serializer.data,
                'token': str(access_token),
            })
        else:
            return Response({
                "bool": False,
                "message": "Invalid Credentials !!!"
            })

#############################################################   Categories   #####################################################################
# Create Category
class AddCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        serializer = admin_serializer.CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'success'
            })

# Fetch All Categories
class AllCategory(APIView):
    def get(self,request):
        categories = models.Categories.objects.all()
        serializer = admin_serializer.CategorySerializer(categories,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Particular Category Details
def CategoryDetails(request,category_id):
    category= models.Categories.objects.get(pk=category_id)
    serialized_data = admin_serializer.CategorySerializer(category).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': CategoryDetails,
        'request': request,
    }
    return response

# Edit Category
class EditCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def put(self, request, category_id):
        try:
            obj = models.Categories.objects.get(pk=category_id)
        except models.Categories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializer.CategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Category Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

# Delete Particular Category
class DeleteCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,category_id):
        category_exist = models.Categories.objects.filter(id = category_id)
        if category_exist:
            categories = models.Categories.objects.get(pk=category_id)
            categories.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Category Deleted Succesfully'
            })
        else:
            return Response({
                'status': 200,
                'bool':False,
                'message': 'No category exist'
            })

#############################################################   Sub Categories   #####################################################################
# Add New Sub categopry
class SubCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        serializer = admin_serializer.SubCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'success'
            })

# Fetch All Sub Categories for particular category
def ParticularCategoriesSubCategoriesList(request,cat_id):
    subcat= models.SubCategories.objects.get(pk=cat_id)
    serialized_data = admin_serializer.SubCategorySerializer(subcat).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ParticularCategoriesSubCategoriesList,
        'request': request,
    }
    return response

# Fetch all Sub Categories for a sub category
class ParticularSubCatsSubcategories(APIView):
    def get(self,request,sub_cat_id):
        sub_categories = models.SubCategories.objects.filter(sub_cat_id = sub_cat_id)
        serializer = admin_serializer.SubCategorySerializer(sub_categories,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Edit Sub Category
class EditSubCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def put(self, request, sub_cat_id):
        try:
            obj = models.SubCategories.objects.get(pk=sub_cat_id)
        except models.SubCategories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializer.SubCategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "SubCategory Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

# Update Sub Category
class DeleteSubCategory(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,sub_cat_id):
        if models.SubCategories.objects.filter(id = sub_cat_id):
            sub_categories = models.SubCategories.objects.get(pk = sub_cat_id)
            sub_categories.delete()
            return Response({
                'status': 200,
                'bool': True,
                'message': 'success'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'success'
            })

#############################################################   Coupons   #####################################################################
# Add Coupons View With Token Authentication
class AddCoupon(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        serializer = admin_serializer.CounponsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            serialized_coupon_id = serializer.data['id']
            #  Saving Categories
            categories = request.data.getlist('categories')
            products = request.data.getlist('products')
            for i in categories:
                cat_serializer = admin_serializer.Add_Coupons_to_CategoriesSerializer(data={'coupon': serialized_coupon_id, 'category': i})
                if cat_serializer.is_valid():
                    cat_serializer.save()
                else:
                    return Response({
                        'status': 403,
                        'errors': cat_serializer.errors,
                        'message': 'some error occurred'
                    })
            # Saving Products
            for j in products:
                prod_serializer = admin_serializer.AddCoupons_to_ProductSerializer(data={'coupon':serialized_coupon_id,'product':j})
                if prod_serializer.is_valid():
                    prod_serializer.save()
                else:
                    return Response({
                        'status': 403,
                        'errors': prod_serializer.errors,
                        'message': 'some error occurred'
                    })

            all_categories = models.AddCouponsToCategories.objects.filter(coupon = serialized_coupon_id)
            all_categories_serializer = admin_serializer.Add_Coupons_to_CategoriesSerializer(all_categories,many=True)

            all_products = models.AddCouponsToProduct.objects.filter(coupon = serialized_coupon_id)
            all_products_serializer = admin_serializer.AddCoupons_to_ProductSerializer(all_products,many=True)
            return Response({
                'status': 200,
                'coupon_data': serializer.data,
                'category_data': all_categories_serializer.data,
                'products_data':all_products_serializer.data,
                'message': 'success'
            })

# Fetch All Coupons With Token
class GetCoupons(APIView):
    def get(self,request):
        coupons = models.Coupons.objects.all()
        serializer = admin_serializer.CouponSerializerWithCategories(coupons,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Get Particular Coupon
def ParticularCouponDetails(request,coupon_id):
    coupons= models.Coupons.objects.get(pk=coupon_id)
    serialized_data = admin_serializer.CounponsSerializer(coupons).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ParticularCouponDetails,
        'request': request,
    }
    return response

# Edit Coupon Details
class EditCouponDetails(APIView):
    authentication_classes = [CustomAuthentication] 
    def put(self, request, coupon_id):
            try:
                obj = models.Coupons.objects.get(pk=coupon_id)
            except models.Coupons.DoesNotExist:
                return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = admin_serializer.CounponsSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "data": serializer.data,
                    "message": "Coupons Updated Succesfully"
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    


# Delete Coupon
class DeleteCoupon(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,coupon_id):
        coupon_details = models.Coupons.objects.filter(id=coupon_id)
        if coupon_details:
            coupon = models.Coupons.objects.get(pk=coupon_id)
            coupon.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Coupon Deleted'
            })
        else:
            return Response({
                'status': 200,
                'bool':False,
                'message': 'No Coupon Found'
            })


#############################################################   Products   #####################################################################
# Add Products View with token authentication
class AddProduct(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self, request):
        serializer = admin_serializer.ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            serialized_product_id = serializer.data['id']
            #  Saving Images
            images = request.data.getlist('images')
            print(images)
            for i in images:
                img_serializer = admin_serializer.ProductImagesSerializer(data={'product': serialized_product_id, 'image': i})
                if img_serializer.is_valid():
                    img_serializer.save()
                else:
                    return Response({
                        'status': 403,
                        'errors': img_serializer.errors,
                        'message': 'some error occurred'
                    })
            all_images = models.ProductImages.objects.filter(product=serialized_product_id)
            all_images_serializer = admin_serializer.ProductImagesSerializer(all_images,many=True)
            return Response({
                'status': 200,
                'data': serializer.data,
                'images':all_images_serializer.data,
                'message': 'success'
            })


# All Products List With Token Authenticatio
class AllProducts(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request):
        products = models.Product.objects.all()
        for product in products:
            product.calculate_rating()
        serializer = admin_serializer.ProductSerializerWithImages(products,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'All Products Fetched Succesfully'
        })
# Particular Product Details With Token Authentication
def ParticularProductDetails(request,product_id):
    product= models.Product.objects.get(pk=product_id)
    product.calculate_rating()
    serialized_data = admin_serializer.ProductSerializerWithImages(product).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ParticularProductDetails,
        'request': request,
    }
    return response


# Edit Product Details For Title and Description
class EditProductDetails(APIView):
    authentication_classes = [CustomAuthentication]
    def put(self,request,product_id):
        try:
            obj = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            return Response({'error':'Object does not exist'},status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializer.ProductSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            previous_images = models.ProductImages.objects.filter(product = serializer.data['id'])
            previous_images.delete()
            images = request.data.getlist('img')
            for i in images:
                img_serializer = admin_serializer.ProductImagesSerializer(data={'product': serializer.data['id'], 'image': i})
                if img_serializer.is_valid():
                    img_serializer.save()
                else:
                    return Response({
                        'status': 200,
                        'data': img_serializer.errors,
                        'message': 'Something went wrong'
                    })
            prouduct_data=models.Product.objects.filter(id=serializer.data['id'])
            prouduct_data.calculate_rating()
            product_data_serializer=admin_serializer.ProductSerializerWithImages(prouduct_data,many=True)
            return Response({
                "status": 200,
                "data": product_data_serializer.data,
                "message": "Product Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete Product
class DeleteProduct(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,product_id):
        product_details = models.Product.objects.filter(id=product_id)
        if product_details:
            product = models.Product.objects.get(pk=product_id)
            product.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Product Deleted Succesfully'
            })
        else:
            return Response({
                'status': 200,
                'bool':False,
                'message': 'No Product Found'
            })



#############################################################   Carousels   #####################################################################

# API View To Add New Carousel
class AddNewCarousel(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        carousel_serializer = admin_serializer.CarouselSerializer(data=request.data)
        if not carousel_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': carousel_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            carousel_serializer.save()
            return Response({
                'status': 200,
                'errors': carousel_serializer.data,
                'message': 'New Carousel Added Succesfully'
            })


# API View To Delete Carousel
class DeleteCarousel(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,carousel_id):
        carousel_details = models.Carousel.objects.filter(id=carousel_id)
        if carousel_details:
            carousel = models.Carousel.objects.get(pk=carousel_id)
            carousel.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Carousel Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'No Carousel Found'
            })




#############################################################   Brands   #####################################################################


# API View To Add Brands
class AddBrand(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        brand_serializer = admin_serializer.BrandsSerializer(data=request.data)
        if not brand_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': brand_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            brand_serializer.save()
            return Response({
                'status': 200,
                'errors': brand_serializer.data,
                'message': 'New Carousel Added Succesfully'
            })



# API View To Delete Brands
class DeleteBrand(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self,request,brand_id):
        brand_exist = models.Brands.objects.filter(id = brand_id)
        if brand_exist:
            brand = models.Brands.objects.get(pk=brand_id)
            brand.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Brand Deleted Succesfully'
            })
        else:
            return Response({
                'status': 400,
                'bool':False,
                'message': 'No Brand Found'
            })



#############################################################   Customer Management   #####################################################################


from enduser import enduser_serializers

class ALLCustomers(APIView):
    def get(self,request):
        all_customers = models.EndUser.objects.all()
        all_customers_serializer = enduser_serializers.EndUserSerializer(all_customers,many=True)
        return Response({
            "status":200,
            "data":all_customers_serializer.data,
            "message":"All Customers Details Fetched"
        })


#############################################################   Replying To Reviews   #####################################################################

# Particular Products All Reviews
def ParticularProductReviews(request,product_id):
    reviews= models.Product.objects.get(pk=product_id)
    serialized_data = admin_serializer.ProductSerializerWithImages(reviews).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ParticularProductReviews,
        'request': request,
    }
    return response

# Give Reply To EndUser For Already Posted Review By Enduser
class ReplyToReview(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request):
        reply_review_serializer = admin_serializer.ReplyToReviewSerializer(data=request.data)
        if not reply_review_serializer.is_valid():
            return Response({
                'status': 403,
                'errors': reply_review_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            reply_review_serializer.save()
            return Response({
                'status': 200,
                'errors': reply_review_serializer.data,
                'message': 'New Carousel Added Succesfully'
            })




#############################################################   Detailed Sales Report   #####################################################################
# All Orders Status API 
class SalesReport(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request):
        orders_placed = models.Orders.objects.filter(order_status = "Order Placed")
        orders_delivered = models.Orders.objects.filter(order_status = "Delivered")
        orders_shipped = models.Orders.objects.filter(order_status = "Shipped")
        orders_canceled = models.Orders.objects.filter(order_status = "Canceled")
        orders_return_request = models.Orders.objects.filter(order_status = "Requested for Return")

        orders_placed_serializer = enduser_serializers.OrdersSerializer(orders_placed,many=True)
        orders_delivered_serializer = enduser_serializers.OrdersSerializer(orders_delivered,many=True)
        orders_shipped_serializer = enduser_serializers.OrdersSerializer(orders_shipped,many=True)
        orders_canceled_serializer = enduser_serializers.OrdersSerializer(orders_canceled,many=True)
        orders_return_request_serializer = enduser_serializers.OrdersSerializer(orders_return_request,many=True)

        return Response({
            "status":200,
            "placed_orders":orders_placed_serializer.data,
            "orders_shipped":orders_shipped_serializer.data,
            "orders_delivered":orders_delivered_serializer.data,
            "orders_canceled":orders_canceled_serializer.data,
            "orders_requested_for_return":orders_return_request_serializer.data,
            "message":"ALL Sales reports Fetched"
        })



# API for products out of stock
class ProductsOutOfStock(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request):
        products_out_of_stock  = models.Product.objects.filter(no_of_products = 0)
        products_out_of_stock_serializer = admin_serializer.ProductSerializer(products_out_of_stock,many=True)
        return Response({
            "status":200,
            "data":products_out_of_stock_serializer.data,
            "message":"Products out of stock fetched"
        })

# API for Products In Stock
class ProductsInStock(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request):
        products_in_stock  = models.Product.objects.exclude(no_of_products = 0)
        products_in_stock_serializer = admin_serializer.ProductSerializer(products_in_stock,many=True)
        return Response({
            "status":200,
            "data":products_in_stock_serializer.data,
            "message":"Products out of stock fetched"
        })

#############################################################   Orders   #####################################################################
# API View for All Orders
class AllOrders(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self,request):
        orders = models.Orders.objects.all()
        orders_serializer = enduser_serializers.OrdersSerializer(orders,many=True)
        return Response({
            "status":200,
            "data":orders_serializer.data,
            "message":"all orders fetched"
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


# Change Order Status
class ChangeOrderStatus(APIView):
    authentication_classes = [CustomAuthentication]
    def post(self,request,order_id):
        order_details = models.Orders.objects.get(pk = order_id)
        order_details.order_status = request.data['order_status']
        order_details.save()
        updated_order_details = models.Orders.objects.filter(id = order_id)
        updated_order_details_serializer = enduser_serializers.OrdersSerializer(updated_order_details,many=True)
        return Response({
            'status': 200,
            'data': updated_order_details_serializer.data,
            'message': 'Order Details Fetched Succesfully'
        })

