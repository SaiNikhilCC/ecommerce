from django.urls import path
from . import views


urlpatterns = [

    # SignUP/LogIN
    path('register-user/', views.RegisterUser.as_view()),
    path('verify-otp/',views.VerifyOtp.as_view()),
    path('resend-otp/',views.ResendOTP.as_view()),
    path('login/',views.Login.as_view()),
    path('user-profile/<user_id>/',views.UserProfile),
    path('edit-user-profile/<str:user_id>/',views.EditUserProfile.as_view()),

    path('users-list/',views.UsersList.as_view()),
    
    # Products
    path("all-products/",views.AllProducts.as_view()),
    path("all-products/<int:product_id>/",views.ParticularProductDetails),

    # CART
    path("add-to-cart/",views.AddToCart.as_view()),
    path("get-users-cart/<str:user_id>/",views.UsersCart.as_view()),

    # ORDERS
    path("create-order/",views.CreateOrders.as_view()),
    path("request-for-order-cancellation/<int:order_id>/",views.RequestOrderCancellation.as_view()),
    path("order-details/<int:order_id>/",views.OrderDetails.as_view()),
    path("orders-history/<str:user_id>/",views.OrdersHistory.as_view()),

    # Wishlist
    path("add-item-to-wishlist/",views.AddToWishlist.as_view()),
    path("users-whishlist/<str:user_id>/",views.UsersWishList.as_view()),
    path("remove-from-wishlist/<int:wishlist_id>/",views.RemoveFromWishlist.as_view()),

    # Reviews
    path("post-review/",views.PostReview.as_view()),
    path("particular-product-reviews/<int:product_id>/",views.ParticularProductReviews.as_view()),
    path("delete-review/<int:review_id>/",views.DeleteReview.as_view()),
    path("replies-received-to-a-particular-review/<int:review_id>/",views.ReceivedReviewsToAParticularReview.as_view()),


    # Search Products
    path("products/",views.SearchProduct.as_view())

]
















