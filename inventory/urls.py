from django.urls import path
from .views import *


urlpatterns=[
    path('create_product/', CreateProductView.as_view()),
    path('list_product/', ProductListView.as_view()),
    path('create_category/', CreateCategoryView.as_view()),
    path('list_category/', ShowAllCategoryView.as_view()),
    path('login/', LoginView.as_view()),
    path('create/', CreateUserView.as_view()),
    path('product_details/<int:pk>/', EachProductInformationView.as_view()),
    path('category_details/<int:pk>/', SingleCategoryDetails.as_view()),
    path('register_suppliers/', RegisterSuppliersView.as_view()),
    path('view_suppliers/', ViewAllSuppliersView.as_view()),
    path('suppliers_details/<int:pk>/', SuppliersDetailsView.as_view()),
    path('stock_level/<int:pk>', StockLevelOfProductView.as_view()),
    # path('list_level/', ListOfProductsStockLevelView.as_view()),
    # path('update_stock/<int:pk>', UpdateStockView.as_view()),
    # path('retrieve_stock/<int:pk>', StockLevelView.as_view()),
    path('orders/', OrdersView.as_view()),
    path('order_list/', AllOrdersView.as_view()),
    path('retrieve_list/<int:pk>', RetrieveOrdersView.as_view()),
    path('log/', InventoryLogView.as_view()),
    path('alert/', LowStockAlertView.as_view()),
    path('alert/', LowStockProductListView.as_view())
]