from django.urls import path
from . import views


urlpatterns = [

    # States
    path('states/', views.StatesList.as_view()),                             # List off All States And Crete New State
    
    # Districts
    path('districts/<int:state_id>/', views.DistrictsList.as_view()),        # Particular States Districts
    path('all-districts/', views.AllDistrictsDetailedView.as_view()),        # All District Irrespective of States
    path('create-districts/', views.CreateDistrictsList.as_view()),          # Create New District

    # Mandals
    path('mandals/<int:district_id>/', views.MandalsList.as_view()),         # Particular Districts Mandal
    path('create-mandals/', views.CreateMandals.as_view()),                  # Create New Mandal
    path('all-mandals/', views.AllMandalsDetailedView.as_view()),            # All Mandals Irrespective of District and States

    # Super Admin Login API View
    path("login/",views.SuperAdminLoginView.as_view()),

    # Categories
    path("add-category/",views.AddCategory.as_view()),
    path("all-category/",views.AllCategory.as_view()),
    path("category-details/<int:category_id>/",views.CategoryDetails),
    path("edit-category/<int:category_id>/",views.EditCategory.as_view()),
    path("delete-category/<int:category_id>/",views.DeleteCategory.as_view()),


    # Sub Caategories
    path("add-sub-category/",views.SubCategory.as_view()),
    path("particular-category-sub-category-list/<int:cat_id>/",views.ParticularCategoriesSubCategoriesList),
    path("particular-sub-category-sub-category-list/<int:sub_cat_id>/",views.ParticularSubCatsSubcategories.as_view()),
    path("edit-sub-category/<int:sub_cat_id>/",views.EditSubCategory.as_view()),
    path("delete-sub-category/<int:sub_cat_id>/",views.DeleteSubCategory.as_view()),


    # Products
    path("add-product/",views.AddProduct.as_view()),
    path("all-products/",views.AllProducts.as_view()),
    path("product-details/<int:product_id>/",views.ParticularProductDetails),
    path("edit-product-details/<int:product_id>/",views.EditProductDetails.as_view()),
    path("delete-product/<int:product_id>/",views.DeleteProduct.as_view()),


    # Coupons
    path("add-coupons/",views.AddCoupon.as_view()),
    path("get-coupons/",views.GetCoupons.as_view()),
    path("get-coupon-details/<int:coupon_id>/",views.ParticularCouponDetails),
    path("edit-coupon-details/<int:coupon_id>/",views.EditCouponDetails.as_view()),
    path("delete-coupon/<int:coupon_id>/",views.DeleteCoupon.as_view()),


    # Carousels
    path("add-carousel/",views.AddNewCarousel.as_view()),
    path("delete-carousel/<int:carousel_id>/",views.DeleteCarousel.as_view()),


    # Add Brands
    path("add-brand/",views.AddBrand.as_view()),
    path("delete-brand/<int:brand_id>/",views.DeleteBrand.as_view()),

    # Customer Management
    path("all-customers/",views.ALLCustomers.as_view()),

    # Reply to review
    path("reply-to-review/",views.ReplyToReview.as_view()),
    path("all-reviews-to-a-product/<int:product_id>/",views.ParticularProductReviews),

    # Sales Report
    path("all-orders-report/",views.SalesReport.as_view()),
    path("products-out-of-stock/",views.ProductsOutOfStock.as_view()),
    path("products-in-stock/",views.ProductsInStock.as_view()),

    # Orders
    path("all-orders/",views.AllOrders.as_view()),
    path("order-details/<int:order_id>/",views.OrderDetails.as_view()),
    path("change-order-status/<int:order_id>/",views.ChangeOrderStatus.as_view()),
]









