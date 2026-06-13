from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductListCreateApiView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        Show all products list
        """
        products = Product.objects.filter(is_active=True).order_by("-id")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductSerializer, responses={201: ProductSerializer()})
    def post(self, request):
        """
        Create a new product
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):

    def get_obj(self, pk):
        """
        Helper to get a product object based on primary key.
        If not found, returns None.
        """
        try:
            return Product.objects.get(pk=pk, is_active=True)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Show details of a specific product
        """
        product = self.get_obj(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductSerializer, responses={200: ProductSerializer()})
    def patch(self, request, pk):
        """
        Partial update of a specific product
        """
        product = self.get_obj(pk)
        if product is None:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductSerializer,responses={200: ProductSerializer()})
    def put(self, request, pk):
        """
        Full edit of a specific product
        """
        product = self.get_obj(pk)
        if product is None:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




