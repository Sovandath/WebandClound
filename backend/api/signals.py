from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase, Inventory

@receiver(post_save, sender=Purchase)
def update_inventory_on_purchase(sender, instance, created, **kwargs):
    if created:
        try: 
            inventory = Inventory.objects.get(product=instance.product)
            inventory.quantity -= instance.quantity
            inventory.save()
        except Inventory.DoesNotExist:
            # Handle the case where inventory does not exist if necessary
            pass  