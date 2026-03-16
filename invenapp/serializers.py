from rest_framework import serializers
from .models import Category, FoodItem, Ingredient, Order, Wastage
# from .models import Products   #TODAYS CLASS

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class FoodItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'category', 'is_available']

# 👇 NEW: Ingredient serializer for inventory UI
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "unit", "stock_qty", "low_stock_alert"]

class WastageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wastage
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

# class ProductSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Products
#         fields = '__all__'