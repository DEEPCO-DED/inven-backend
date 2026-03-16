from django.db import models
from django.utils import timezone


# ---------------------------
# Food Category (Breakfast, Drinks, Snacks, etc)
# ---------------------------
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ---------------------------
# Food Item (What customer sees in menu)
# ---------------------------
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ---------------------------
# Ingredient (Real stock in kitchen)
# ---------------------------
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20)  # pcs, grams, ml, kg
    stock_qty = models.FloatField(default=0)  # how much stock available
    low_stock_alert = models.FloatField(default=0)  # alert threshold

    def __str__(self):
        return f"{self.name} ({self.stock_qty} {self.unit})"


# ---------------------------
# Recipe (Mapping food to ingredients)
# Example:
# Bun Maska → Bun (1 pc)
# Bun Maska → Butter (10 g)
# ---------------------------
class Recipe(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name="recipes")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_used = models.FloatField()  # how much ingredient used for 1 food item

    def __str__(self):
        return f"{self.food_item.name} - {self.ingredient.name}"


# add wastage
class Wastage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="wastages")
    quantity = models.FloatField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Waste: {self.ingredient.name} - {self.quantity} {self.ingredient.unit}"
    

class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ("DINE_IN", "Dine In"),
        ("TAKE_AWAY", "Take Away"),
    )
    PAYMENT_MODE_CHOICES = (
        ("COD", "Cash On Delivery"),
        ("ONLINE", "Online"),
    )

    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)    


# TODAYS CLASS
# class Products(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     price = models.IntegerField()
#     stock = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nmame
        