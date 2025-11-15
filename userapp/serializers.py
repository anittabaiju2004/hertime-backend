from rest_framework import serializers
from adminapp.models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = '__all__'
from rest_framework import serializers
from .models import tbl_register

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_register
        fields = '__all__'

from rest_framework import serializers
from .models import tbl_register

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


from rest_framework import serializers
from .models import CycleInput

class CycleInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CycleInput
        fields = '__all__' 



from adminapp.models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"


from rest_framework import serializers
from adminapp.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        # This includes: id, category, name, description, quantity, price, image, created_at, category_name

    def get_image(self, obj):
        # return the media-relative path (e.g. "/media/...")
        if obj.image:
            return obj.image.url  # typically starts with '/media/...'
        return None







#cart and booking serializers
from rest_framework import serializers
from .models import ProductBooking, BookingPayment, Cart, CartPayment

class ProductBookingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    user_name = serializers.CharField(source='user.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ProductBooking
        fields = [
            'id', 'user_id', 'user_name',
            'product_id', 'product_name', 'category_name',
            'quantity', 'total_price', 'status', 'booking_date'
        ]

class BookingPaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    product_name = serializers.CharField(source='booking.product.name', read_only=True)

    class Meta:
        model = BookingPayment
        fields = [
            'id', 'payment_choice',
            'booking', 'user', 'user_name', 'product_name',
            'payment_type', 'status',
            'card_holder_name', 'card_number', 'expiry_date', 'cvv',
            'total_amount', 'created_at'
        ]


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user_id', 'product_id',
            'product_name', 'product_image', 'category_name',
            'quantity', 'total_price', 'status', 'created_at'
        ]


class CartPaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = CartPayment
        fields = [
            'id', 'payment_choice',
            'user', 'user_name', 'cart_ids',
            'payment_type', 'status',
            'card_holder_name', 'card_number', 'expiry_date', 'cvv',
            'total_amount', 'created_at'
        ]
