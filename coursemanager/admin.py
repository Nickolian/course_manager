from django.contrib import admin
from .models import Product, Lesson, Group


class LessonInLine(admin.TabularInline):
    model = Lesson
    extra = 0


class GroupInLine(admin.StackedInline):
    model = Group
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [LessonInLine, GroupInLine]


class GroupAdmin(admin.ModelAdmin):
    list_display = ["title"]
    filter_horizontal = ["students"]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson)
admin.site.register(Group, GroupAdmin)
