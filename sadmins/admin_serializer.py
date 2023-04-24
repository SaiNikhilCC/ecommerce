from rest_framework import serializers
from main import models
import random
import uuid


# States Serializer
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ['id', 'state_representing_image', 'state_name']
        depth = 1

class CreateStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ['id', 'state_representing_image', 'state_name']

# District Serializer
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disrtict
        fields = '__all__'
        depth = 1

class CreateDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disrtict
        fields = '__all__'

class AllDistrictsDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disrtict
        fields = '__all__'
        depth=1


# Mandals Serializer
class MAndalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'
        depth = 1

class CreateMandalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'

class AllMandalsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'
        depth = 2


class SuperAdminAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SuperAdminAcc
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
    def create(self,validated_data):
        product = models.Product.objects.create(sku_code=validated_data['sku_code'],product_title=validated_data['product_title'], description=validated_data['description'],category = validated_data['category'],sub_category = validated_data['sub_category'], no_of_products = validated_data['no_of_products'], actual_price = validated_data['actual_price'], selling_price = validated_data['selling_price'],color = validated_data['color'],brand_id = validated_data['brand'].id)
        product.save()
        return product


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImages
        fields = "__all__"
    def create(self, validated_data):
        image_product = models.ProductImages.objects.create(product = validated_data['product'],image =validated_data['image'] )
        image_product.save()
        return image_product


class ProductSerializerWithImages(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True,read_only = True)
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = "__all__"
    def create(self,validated_data):
        category = models.Categories.objects.create(category=validated_data['category'],category_image = validated_data['category_image'])
        category.save()
        return category


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategories
        fields = "__all__"
    def create(self,validated_data):
        sub_category = models.SubCategories.objects.create(sub_category_img = validated_data['sub_category_img'],category=validated_data['category'],sub_cat_id = validated_data['sub_cat_id'],sub_category = validated_data['sub_category'])
        sub_category.save()
        return sub_category


class CounponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupons
        fields = "__all__"
    def create(self, validated_data):
        coupon = models.Coupons.objects.create(coupon_code = validated_data['coupon_code'], coupon_description = validated_data['coupon_description'],discount_percentage = validated_data['discount_percentage'],min_price_for_coupon_avail = validated_data['min_price_for_coupon_avail'], max_price = validated_data['max_price'], no_of_days_valid = validated_data['no_of_days_valid'], no_of_coupons = validated_data['no_of_coupons'], universal_coupon = validated_data['universal_coupon'] )
        coupon.save()
        return coupon


class Add_Coupons_to_CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddCouponsToCategories
        fields="__all__"
    def create(self, validated_data):
        cat_cou = models.AddCouponsToCategories.objects.create(coupon=validated_data['coupon'], category = validated_data['category'])
        cat_cou.save()
        return cat_cou


class AddCoupons_to_ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddCouponsToProduct
        fields = "__all__"
    def create(self,validated_data):
        prod_cou = models.AddCouponsToProduct.objects.create(coupon = validated_data['coupon'], product = validated_data['product'])
        prod_cou.save()
        return prod_cou


class CouponSerializerWithCategories(serializers.ModelSerializer):
    coupon_add_coupon_to_category = Add_Coupons_to_CategoriesSerializer(many=True,read_only = True)
    coupon_add_coupon_to_product = AddCoupons_to_ProductSerializer(many=True,read_only = True)
    class Meta:
        model = models.Coupons
        fields = "__all__"
        depth = 1

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carousel
        fields = "__all__"

    def create(self,validated_data):
        carousel = models.Carousel.objects.create(carousel_image = validated_data['carousel_image'], navigation_link = validated_data['navigation_link'])
        carousel.save()
        return carousel


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brands
        fields = "__all__"

    def create(self,validated_data):
        brand = models.Brands.objects.create(brand_name = validated_data['brand_name'], brand_logo = validated_data['brand_logo'])
        brand.save()
        return brand


class ReplyToReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReplyReviews
        fields = "__all__"
    
    def create(self, validated_data):
        reply_review = models.ReplyReviews.objects.create(review = validated_data['review'],reply_text = validated_data['reply_text'])
        reply_review.save()
        return reply_review













