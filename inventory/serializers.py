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


class ProductSerializer(serializers.Serializer):
     class Meta:
          model=Product
          fields='__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'

