from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from django.db.models import Sum

from .models import Order, Category, FoodItem, Ingredient
from .serializers import (
    CategorySerializer,
    FoodItemSerializer,
    IngredientSerializer,
    WastageSerializer,
    OrderSerializer,
)
# from .models import Products    #TODAYS CLASS
# from  .serializers import ProductSerializer

# -----------------------------
# Menu APIs
# -----------------------------

@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def food_list(request):
    category_id = request.GET.get('category_id')

    foods = FoodItem.objects.select_related("category").all()

    if category_id:
        foods = foods.filter(category_id=int(category_id))

    serializer = FoodItemSerializer(foods, many=True)
    return Response(serializer.data)

# -----------------------------
# Inventory APIs (Employee UI)
# -----------------------------

@api_view(['GET'])
def ingredients_list(request):
    """
    List all ingredients for employee inventory screen
    """
    ingredients = Ingredient.objects.all().order_by("name")
    serializer = IngredientSerializer(ingredients, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_stock(request):
    """
    Body: { "id": 1, "add_qty": 500 }
    Adds stock to an ingredient
    """
    ing_id = request.data.get("id")

    try:
        add_qty = float(request.data.get("add_qty", 0))
    except (TypeError, ValueError):
        return Response(
            {"error": "add_qty must be a number"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not ing_id or add_qty <= 0:
        return Response(
            {"error": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        ingredient = Ingredient.objects.get(id=ing_id)
    except Ingredient.DoesNotExist:
        return Response(
            {"error": "Ingredient not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    ingredient.stock_qty += add_qty
    ingredient.save()

    return Response(
        IngredientSerializer(ingredient).data,
        status=status.HTTP_200_OK
    )


# -----------------------------
# Wastage
# -----------------------------

class AddWastageView(APIView):
    def post(self, request):
        serializer = WastageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Wastage recorded successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Orders
# -----------------------------

class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Order placed"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Reports / Analytics
# -----------------------------

class TodaySalesView(APIView):
    def get(self, request):
        today = now().date()
        orders = Order.objects.filter(created_at__date=today)

        total = orders.aggregate(total=Sum("total_amount"))["total"] or 0
        dine_in = orders.filter(order_type="DINE_IN").aggregate(t=Sum("total_amount"))["t"] or 0
        take_away = orders.filter(order_type="TAKE_AWAY").aggregate(t=Sum("total_amount"))["t"] or 0
        cod = orders.filter(payment_mode="COD").aggregate(t=Sum("total_amount"))["t"] or 0

        return Response({
            "total": total,
            "dineIn": dine_in,
            "takeAway": take_away,
            "cod": cod,
        }, status=status.HTTP_200_OK)
    

# #TODAYS CLASS
# @api_view(['GET'])
# def product_list(request):
#     products = Products.objects.all()  #FETCH ALL PRODUCTS
#     serializer = ProductSerializer(products,many=True)
#     return Response(serializer.data)
    
# #POST- CREATE PRODUCT

# @api_view(['POST'])
# def product_create(request):

#     serializer = ProductSerializer(data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
    
#     return Response(serializer.errors)