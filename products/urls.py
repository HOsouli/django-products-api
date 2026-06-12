from django.urls import path
from .views import ProductListCreateApiView,ProductDetailAPIView

app_name = 'products'

urlpatterns = [
    path('', ProductListCreateApiView.as_view(), name='product_list_create'),
    path('<int:pk>/',ProductDetailAPIView.as_view(), name='product_detail'),
]


