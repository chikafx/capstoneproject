from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User= get_user_model()

class UserSerializer(serializers.ModelSerializer):
    re_password=serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    password= serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model=User
        fields='__all__'
        extra_kwargs={
            'password':{'write_only':True},
            're_password':{'write_only':True}
        }

    def validate(self, attrs):
            max=10
            if len(attrs['password'])<max:
                raise serializers.ValidationError('Password must be at least 10 characters')
            if attrs['password']!=attrs['re_password']:
                raise serializers.ValidationError('Password and re_password must be same')
            return super().validate(attrs)
    def create(self,data):
         User.objects.create_user(
              **data
         )


class LoginSerializer(serializers.Serializer):
     email=serializers.EmailField()
     password=serializers.CharField(style={'input_type':'password'},write_only=True)


class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model=Product
          fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model=Category
          fields='__all__'


class SupplierSerializer(serializers.ModelSerializer):
     class Meta:
          model=Supplier
          fields='__all__'



class StockProductSerializer(serializers.ModelSerializer):
     class Meta:
          model=Product
          fields= '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        order = Order.objects.create(product_id=product_id,  **validated_data)
        return order
#  Retrieve a list of products that are below the minimum stock threshold.
class StockThresholdSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = ['id', 'name', 'stock', 'min_stock']

class InventorySerializer(serializers.ModelSerializer):
     class Meta:
          model=InventoryLog
          fields='__all__'

