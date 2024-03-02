from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"products_api", views.ProductViewSet, basename="products_api")
router.register(r"detail_product", views.DetailProductViewSet, basename="detail_product")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
    path("api/lessons", views.LessonsViewSet.as_view(), name="lessons_api"),
]
