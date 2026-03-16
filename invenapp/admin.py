from django.contrib import admin
from .models import Category, FoodItem, Ingredient, Recipe,Wastage

# This allows you to add ingredients directly inside a food item page
class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 1  # how many empty rows to show by default


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name",)
    inlines = [RecipeInline]  # Show recipe editor inside FoodItem admin


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "stock_qty", "unit", "low_stock_alert")
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("food_item", "ingredient", "quantity_used")

admin.site.register(Wastage)