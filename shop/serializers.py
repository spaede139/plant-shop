from rest_framework import serializers
from .models import Product, Category, Manufacturer, Cart, CartItem
from django.contrib.auth.models import User
from .models import Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name')
    
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = '__all__'
    
    def get_item_total(self, obj):
        return obj.item_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Cart
        fields = '__all__'
    
    def get_total_price(self, obj):
        return obj.total_price()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'full_name', 'phone', 'address', 'favorite_category', 'city', 'role', 'created_at']
        read_only_fields = ['user', 'role', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'full_name', 'phone']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    
    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        phone = validated_data.pop('phone', '')
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        if full_name:
            user.profile.full_name = full_name
        if phone:
            user.profile.phone = phone
        user.profile.save()
        
        return user