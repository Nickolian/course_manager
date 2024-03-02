from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Product, Lesson, Subscription
from .serializers import ProductSerializer, LessonSerializer, DetailedProductSerializer


def index(request):
    user = request.user
    return render(request, "coursemanager/index.html")


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonsViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        user_products = Subscription.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        if not user_products:
            return Response("У вас нет доступа к продуктам", status=status.HTTP_403_FORBIDDEN)
        return Lesson.objects.filter(product__in=user_products)


class DetailProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = DetailedProductSerializer
