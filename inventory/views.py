from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import response, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, action


# # views for user registration
class CreateUserView(APIView):

    """
    this is a view used to create a user in this section

    NB:this view is not protected
    """
    @swagger_auto_schema(method="post", request_body=UserSerializer )
    @action(detail=True, methods=['post'])

    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('re_password')
        serializer.save()

        return Response(serializer.data, status=201)






class UserListView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    
   
# views for login
class LoginView(APIView):
    """
    this is a view used to create a user in this section to login NB:this view is not protected
    """
    @swagger_auto_schema(method='post', request_body=UserSerializer)
    @action(detail=True, methods=['post'])

    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=authenticate(request,email=serializer.validated_data['email'],
                              password=serializer.validated_data['password'])
            if user:
                try:
                    refresh_token=RefreshToken.for_user(user)
                    data={}
                    data['id']=user.pk
                    data['first_name']=user.first_name
                    data['last_name']=user.last_name
                    data['access_token']=str(refresh_token.access_token)
                    data['refresh_token']=str(refresh_token)

                    return Response(data, status=200)
                except Exception as error:
                    return Response(
                        {
                            'error': f"{error}"
                        },
                        status=400
                    ) 
            else:
                    data={
                        'error': 'invalid login credentials'
                    }
                    return Response(data, status=401)
        else:
                data={
                    'error':serializer.errors
                }
                return Response(data, status=400)



# views for logout
class logoutView(APIView):
    def post(self, request):
        return response.Response({'message':'logout successful'})
    
# - **POST**: Create a new product with details like name, description, category, price, and SKU.
class CreateProductView(generics.CreateAPIView):
     serializer_class= ProductSerializer
     queryset= Product.objects.filter()


class CreateCategoryView(generics.CreateAPIView):
     serializer_class= CategorySerializer
     queryset=Category.objects.filter()

class ShowAllCategoryView(generics.ListAPIView):
     serializer_class= CategorySerializer
     queryset=Category.objects.filter()

class SingleCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
     serializer_class=CategorySerializer
     queryset=Category
     lookup_field='pk'

# list all products
class ProductListView(generics.ListAPIView):
     serializer_class=ProductSerializer
     queryset=Product.objects.filter()

class EachProductInformationView(generics.RetrieveUpdateDestroyAPIView):
     serializer_class=ProductSerializer
     queryset=Product.objects.all()
     lookup_field='pk'
        
# Add a new supplier with details like name, contact information, and address.(POST)
class RegisterSuppliersView(generics.CreateAPIView):
     serializer_class=SupplierSerializer
     queryset=Supplier.objects.filter()

# Retrieve a list of all suppliers.(GET)
class ViewAllSuppliersView(generics.ListAPIView):
     serializer_class=SupplierSerializer
     queryset=Supplier.objects.filter()

class SuppliersDetailsView(generics.RetrieveUpdateDestroyAPIView):
     serializer_class=SupplierSerializer
     queryset=Supplier.objects.all()
     lookup_field='pk'



# # Adjust stock levels for a product (e.g., when new stock is received or items are sold).(POST)
class StockLevelOfProductView(generics.UpdateAPIView):
     serializer_class=ProductSerializer
     queryset=Product.objects.all()
     lookup_field='pk'
     def put(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = request.data.get('quantity')
        adjustment_type = request.data.get('adjustment_type')

        if not quantity or not adjustment_type:
            return Response({'error': 'Quantity and adjustment type are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if adjustment_type == 'stock_in':
                product.receive_stock(quantity)
            elif adjustment_type == 'stock_out':
                product.sell_stock(quantity)
            else:
                return Response({'error': 'Invalid adjustment type'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'Stock adjusted successfully'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Retrieve a list of all products with their current stock levels.(GET)
# class ListOfProductsStockLevelView(generics.ListAPIView):
#      serializer_class=StockProductSerializer
#      queryset=Stock.objects.filter()

# # Update stock quantity for a specific product.(PUT)
# class UpdateStockView(generics.UpdateAPIView):
#      serializer_class=StockProductSerializer
#      queryset=Stock.objects.all()
#      lookup_field='pk'

# # Retrieve stock level for a specific product.
# class StockLevelView(generics.RetrieveAPIView):
#      serializer_class=StockProductSerializer
#      queryset=Stock.objects.all()
#      lookup_field='pk'
     
# Create a new order with details like product_id, quantity, and customer information.
class OrdersView(generics.CreateAPIView):
     serializer_class=OrderSerializer
     queryset=Order.objects.all()

#  Retrieve a list of all orders.
class AllOrdersView(generics.ListAPIView):
     serializer_class=OrderSerializer
     queryset=Order.objects.filter()


#  **GET**: Retrieve details for a specific order, including order status and items.
# - **PUT**: Update order status (e.g., mark as completed, canceled, etc.).
# - **DELETE**: Cancel an order.

class RetrieveOrdersView(generics.RetrieveUpdateDestroyAPIView):
     serializer_class=OrderSerializer
     queryset=Order.objects.all()
     lookup_field='pk'

# - **GET**: Retrieve a log of all inventory adjustments, such as stock-ins, stock-outs, and orders fulfilled.
class InventoryLogView(generics.ListAPIView):
     queryset=InventoryLog.objects.filter()
     serializer_class=InventorySerializer

# **GET**: Retrieve a list of products that are below the minimum stock threshold.
class LowStockAlertView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(stock__lt=models.F('min_stock'))

class LowStockProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(stock__lt=models.F('min_stock'))