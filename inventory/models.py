from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class CustomUser (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=200, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = UserManager()


class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=30)
    contact = models.IntegerField(unique=True)
    address = models.CharField(unique=True, max_length=250)


class Category(models.Model):
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# - **POST**: Create a new product with details like name, description, category, price, and SKU.
class Product(models.Model):
    name = models.CharField(max_length=250, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=0)
    SKU = models.IntegerField(unique=True)

    def __str__(self):
        return self.name
#  Adjust stock levels for a product (e.g., when new stock is received or items are sold).
    def adjust_stock(self, quantity, adjustment_type):
        """ Adjust the stock level of the product.
        
        :param quantity: The number of items to adjust.
        :param adjustment_type: Type of adjustment ('stock_in' or 'stock_out').
        """
        if adjustment_type == 'stock_in':
            self.stock += quantity
        elif adjustment_type == 'stock_out':
            if quantity > self.stock:
                raise ValueError("Not enough stock to complete this operation.")
            self.stock -= quantity
        self.save()

    def receive_stock(self, quantity):
        """Increase stock levels when new stock is received."""
        self.adjust_stock(quantity, 'stock_in')

    def sell_stock(self, quantity):
        """Decrease stock levels when items are sold."""
        self.adjust_stock(quantity, 'stock_out')



# class Stock(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     last_updated = models.DateTimeField(auto_now=True)

# Create a new order with details like product_id, quantity, and customer information.
class Order(models.Model):
    product_id = models.IntegerField()
    order_status=models.CharField(max_length=20, choices=[ ('pending', 'Pending'), ('processed', 'Processed'), ('shipped', 'Shipped'), ('delivered', 'Delivered') ], default='pending')
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    Customers_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(unique=True, null=True)
    gender = models.CharField(max_length=10)
    address= models.CharField(max_length=100)
# /api/inventory/logs/
# - **GET**: Retrieve a log of all inventory adjustments, such as stock-ins, stock-outs, and orders fulfilled.
class InventoryLog(models.Model):
    ADJUSTMENT_CHOICES = [
        ('stock_in', 'Stock In'),
        ('stock_out', 'Stock Out'),
        ('order_fulfilled', 'Order Fulfilled'),
    ]

    adjustment_type = models.CharField(
     max_length=20, choices=ADJUSTMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_adjustment_type_display()} - {self.quantity} - {self.date}"


# class InventoryLog(models.Model):
#     product_id = models.IntegerField()
#     quantity = models.PositiveIntegerField()
#     order_id = models.PositiveIntegerField()
#     log_type = models.CharField(max_length=20, choices=[('stock-in', 'stock-in'),('stock-out', 'stock-out'),('order-fulfilled','order-fulfilled')])
#     created_at = models.DateTimeField(auto_now_add=True)


# ### /api/alerts/low-stock/
# - **GET**: Retrieve a list of products that are below the minimum stock threshold.
class LowStockAlert(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    threshold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
