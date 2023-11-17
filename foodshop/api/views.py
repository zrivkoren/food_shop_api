from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.models import Category, Product, Cart
from .serializers import CategorySerializer, ProductsSerializer, CartSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print("enter to create in cart")
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=401)
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        new_quantity = request.data.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(Cart, user=request.user, product=product)
        cart_item.quantity = new_quantity
        cart_item.save()
        return Response({"message": "Product quantity updated successfully"}, status=200)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(Cart, user=request.user, product=product)
        cart_item.delete()
        return Response({"message": "Product removed from cart successfully"}, status=200)

    @action(methods=['delete'], detail=False)
    def clear(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=204)
