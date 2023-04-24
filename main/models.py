from django.db import models
import uuid

# UserBase Model
class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=100)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

#############################################################   Super Admin Models   #####################################################################
# Categories
class Categories(models.Model):
    category = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to="category_images/")
    def __str__(self):
        return self.category

# Sub Categories
class SubCategories(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_cat_id = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    sub_category = models.CharField(max_length=200)
    sub_category_img = models.ImageField(upload_to='sub_cat_images/',null=True)
    def __str__(self):
        return self.sub_category

# Super Admin Account
class SuperAdminAcc(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

# Brands
class Brands(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_logo = models.ImageField(upload_to="brnad_logos/")

from django.db.models import Avg


# Products
class Product(models.Model):
    product_title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    sku_code = models.CharField(max_length=200,unique=True)
    no_of_products = models.IntegerField()
    actual_price = models.IntegerField()
    selling_price = models.IntegerField()
    brand = models.ForeignKey(Brands,on_delete=models.CASCADE)
    color = models.CharField(max_length=200)
    no_of_orders = models.IntegerField(default=0)
    no_of_wishlists = models.IntegerField(default=0)
    no_of_cart = models.IntegerField(default=0)
    no_of_returned = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='product_thumbnails/')
    rating = models.IntegerField(default=0)
    numReviews = models.IntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

    def calculate_rating(self):
        ratings = Reviews.objects.filter(product=self)
        if ratings.count() > 0:
            self.rating = ratings.aggregate(Avg('rating'))['rating__avg']
            self.numReviews = ratings.count()
        else:
            self.rating = 0
            self.numReviews = 0
        self.save()
  
# Product Images
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to="product_images/")

# Product Coupons
class Coupons(models.Model):
    coupon_code = models.CharField(max_length=200)
    coupon_description = models.TextField()
    discount_percentage = models.IntegerField()
    min_price_for_coupon_avail = models.IntegerField()
    max_price = models.IntegerField()
    no_of_days_valid = models.CharField(max_length=200)
    no_of_coupons = models.IntegerField()
    universal_coupon = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    def __str__(self):
        return self.coupon_code

# Adding Coupons to Products
class AddCouponsToProduct(models.Model):
    coupon = models.ForeignKey(Coupons,on_delete=models.CASCADE,related_name="coupon_add_coupon_to_product")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

# Adding Products to Categories
class AddCouponsToCategories(models.Model):
    coupon = models.ForeignKey(Coupons,on_delete=models.CASCADE,related_name="coupon_add_coupon_to_category")
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)

# Class Product Type API
class ProductType(models.Model):
    type = models.CharField(max_length=200)
    date_created = models.DateField

# Class Carousels
class Carousel(models.Model):
    carousel_image = models.ImageField(upload_to="carousel_images/")
    navigation_link = models.CharField(max_length=500,null=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)





#############################################################   End User Models   #####################################################################

# End User 
class EndUser(UserBaseModel):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="user_profiles/",null=True)
    otp = models.CharField(max_length=100,null=True)
    is_verified  = models.BooleanField(default=False)
    dob = models.DateField(max_length=8,null=True)
    def __str__(self):
        return self.name


# Cart Items
class CartItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


# State
class State(models.Model):
    state_name = models.CharField(max_length=200)
    state_representing_image = models.ImageField(upload_to="state_images/",null=True)


# District 
class Disrtict(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    district_name = models.CharField(max_length=200)


# Mandal
class Mandal(models.Model):
    district = models.ForeignKey(Disrtict,on_delete=models.CASCADE)
    mandal_name = models.CharField(max_length=200)


# End Users Orders
class Orders(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchased_price = models.IntegerField()
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    disrtict = models.ForeignKey(Disrtict,on_delete=models.CASCADE)
    mandal = models.ForeignKey(Mandal,on_delete=models.CASCADE)
    hno = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    colony = models.CharField(max_length=500)
    landmark = models.CharField(max_length=200,null=True)
    order_status = models.CharField(max_length=200,default="Order Placed")
    mode_of_payment = models.CharField(max_length=200)
    order_placed_date = models.DateField(auto_now_add=True)
    order_placed_time = models.TimeField(auto_now_add=True)
    order_updated_date = models.DateField(auto_now=True)
    order_updated_time = models.TimeField(auto_now=True)


# Delivery Address
# class DeliveryAddress(models.Model):
#     user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
#     address = models.TextField()


# End User Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)


# Reviews
class Reviews(models.Model):
    user = models.ForeignKey(EndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200,null=True)
    description = models.TextField()
    ratings = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Reply Reviews
class ReplyReviews(models.Model):
    review = models.ForeignKey(Reviews,on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)




 






