from django.urls import path
from . import views  

urlpatterns = [
    path("categories/",views.categories_list),
    path("foods/", views.food_list),

    path("ingredients/", views.ingredients_list),
    path("stock/add/", views.add_stock),

    path("wastage/add/", views.AddWastageView.as_view()),

    path("orders/create/", views.CreateOrderView.as_view()),
    path("today-sales/", views.TodaySalesView.as_view()),
    # TODAYS
    # path('api/products/',views.product_list),
    # path('api/products/create/',views.product_create),
]