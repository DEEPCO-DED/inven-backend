from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wastage, Ingredient

@receiver(post_save, sender=Wastage)
def reduce_stock_on_wastage(sender, instance, created, **kwargs):
    if created:
        ingredient = instance.ingredient
        ingredient.stock_qty -= instance.quantity
        if ingredient.stock_qty < 0:
            ingredient.stock_qty = 0
        ingredient.save()