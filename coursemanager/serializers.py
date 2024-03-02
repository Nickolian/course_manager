from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from rest_framework import serializers
from .models import Product, Lesson, Subscription


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["author", "title", "price", "start_date", "lessons_count"]

    def get_lessons_count(self, product):
        return product.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ["product_title", "title"]


class DetailedProductSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    product_students = serializers.SerializerMethodField()
    groups_fill_percent = serializers.SerializerMethodField()
    product_subscribe_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["author_username", "title", "price", "start_date", "product_students", "groups_fill_percent",
                  "product_subscribe_percent"]

    def get_product_students(self, product):
        return product.groups_product.annotate(product_students=Count("students")).aggregate(total=Count("students"))[
            'total']

    def get_groups_fill_percent(self, product):
        groups = product.groups_product.annotate(product_students=Count("students"))
        if groups:
            fill_percent = groups.aggregate(fill=Avg("product_students"))['fill'] / product.max_students * 100
            return fill_percent
        return 0

    def get_product_subscribe_percent(self, product):
        user = get_user_model()
        total_students = user.objects.count()
        total_subscriptions = Subscription.objects.filter(product=product).count()
        return total_subscriptions / total_students * 100
