from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    Purchase, Inventory, Invoice, Transaction, ActivityLog,
    Product, Category, SubCategory, Source, NewStock, Customer, User
)

# Store the previous status of invoice before update
_invoice_previous_status = {}
# Store previous states for activity logging
_model_previous_states = {}

@receiver(post_save, sender=Purchase)
def update_inventory_on_purchase(sender, instance, created, **kwargs):
    """
    Automatically reduce inventory when a purchase is created.
    This signal is triggered when creating invoices with line items.
    """
    if created:
        try: 
            inventory = Inventory.objects.get(product=instance.product)
            
            # Check if there's enough stock
            if inventory.quantity < instance.quantity:
                raise ValidationError(
                    f"Insufficient stock for {instance.product.productName}. "
                    f"Available: {inventory.quantity}, Requested: {instance.quantity}"
                )
            
            inventory.quantity -= instance.quantity
            inventory.save()
        except Inventory.DoesNotExist:
            # Handle the case where inventory does not exist
            raise ValidationError(
                f"No inventory record found for product: {instance.product.productName}"
            )


@receiver(pre_save, sender=Invoice)
def store_previous_invoice_status(sender, instance, **kwargs):
    """
    Store the previous status of the invoice before it's updated.
    This allows us to detect status changes in the post_save signal.
    """
    if instance.pk:  # Only for existing invoices (updates)
        try:
            previous = Invoice.objects.get(pk=instance.pk)
            _invoice_previous_status[instance.pk] = previous.status
        except Invoice.DoesNotExist:
            pass


@receiver(post_save, sender=Invoice)
def create_transaction_on_invoice_paid(sender, instance, created, **kwargs):
    """
    Automatically create a transaction when an invoice status changes to 'Paid'.
    This tracks when an invoice transitions from any status (Draft, Unpaid) to 'Paid'.
    """
    # Get the previous status
    previous_status = _invoice_previous_status.get(instance.pk)
    
    # Only process if invoice already exists (not being created) and status changed to 'Paid'
    if not created and instance.status == 'Paid' and previous_status != 'Paid':
        # Check if a completed transaction already exists for this invoice
        existing_transaction = Transaction.objects.filter(
            invoice=instance,
            transactionStatus='Completed'
        ).first()
        
        # Only create if no completed transaction exists
        if not existing_transaction:
            Transaction.objects.create(
                invoice=instance,
                customer=instance.customer,
                amountPaid=instance.grandTotal,
                paymentMethod=instance.paymentMethod,
                transactionStatus='Completed',
                paymentReference=instance.qrReference,
                transactionDate=timezone.now(),
                recordedByUser=instance.createdByUser
            )
    
    # Clean up the stored previous status
    if instance.pk in _invoice_previous_status:
        del _invoice_previous_status[instance.pk]


# ==================== ACTIVITY LOGGING ====================

def get_current_user_from_instance(instance):
    """Helper function to extract user from various model instances."""
    user_fields = ['createdByUser', 'addedByUser', 'recordedByUser']
    for field in user_fields:
        if hasattr(instance, field):
            user = getattr(instance, field)
            if user:
                return user
    return None


# ----- Product Activity Logging -----
@receiver(post_save, sender=Product)
def log_product_activity(sender, instance, created, **kwargs):
    """Log when products are created or updated."""
    user = get_current_user_from_instance(instance)
    
    if created:
        ActivityLog.objects.create(
            user=user,
            actionType='CREATE_PRODUCT',
            description=f"Created product: {instance.productName} (SKU: {instance.skuCode})"
        )
    else:
        ActivityLog.objects.create(
            user=user,
            actionType='UPDATE_PRODUCT',
            description=f"Updated product: {instance.productName} (SKU: {instance.skuCode})"
        )


@receiver(post_delete, sender=Product)
def log_product_deletion(sender, instance, **kwargs):
    """Log when products are deleted."""
    ActivityLog.objects.create(
        user=None,
        actionType='DELETE_PRODUCT',
        description=f"Deleted product: {instance.productName} (SKU: {instance.skuCode})"
    )


# ----- Category Activity Logging -----
@receiver(post_save, sender=Category)
def log_category_activity(sender, instance, created, **kwargs):
    """Log when categories are created or updated."""
    if created:
        ActivityLog.objects.create(
            user=None,
            actionType='CREATE_CATEGORY',
            description=f"Created category: {instance.name}"
        )
    else:
        ActivityLog.objects.create(
            user=None,
            actionType='UPDATE_CATEGORY',
            description=f"Updated category: {instance.name}"
        )


@receiver(post_delete, sender=Category)
def log_category_deletion(sender, instance, **kwargs):
    """Log when categories are deleted."""
    ActivityLog.objects.create(
        user=None,
        actionType='DELETE_CATEGORY',
        description=f"Deleted category: {instance.name}"
    )


# ----- Inventory Activity Logging -----
@receiver(pre_save, sender=Inventory)
def store_previous_inventory_quantity(sender, instance, **kwargs):
    """Store previous inventory quantity for comparison."""
    if instance.pk:
        try:
            previous = Inventory.objects.get(pk=instance.pk)
            _model_previous_states[f'inventory_{instance.pk}'] = previous.quantity
        except Inventory.DoesNotExist:
            pass


@receiver(post_save, sender=Inventory)
def log_inventory_activity(sender, instance, created, **kwargs):
    """Log when inventory is created or updated."""
    if created:
        ActivityLog.objects.create(
            user=None,
            actionType='CREATE_INVENTORY',
            description=f"Created inventory for: {instance.product.productName} - Quantity: {instance.quantity} @ {instance.location}"
        )
    else:
        previous_qty = _model_previous_states.get(f'inventory_{instance.pk}')
        if previous_qty is not None and previous_qty != instance.quantity:
            change = instance.quantity - previous_qty
            change_text = f"+{change}" if change > 0 else str(change)
            ActivityLog.objects.create(
                user=None,
                actionType='UPDATE_INVENTORY',
                description=f"Inventory adjusted for {instance.product.productName}: {previous_qty} → {instance.quantity} ({change_text})"
            )
        # Clean up
        if f'inventory_{instance.pk}' in _model_previous_states:
            del _model_previous_states[f'inventory_{instance.pk}']


# ----- NewStock Activity Logging -----
@receiver(post_save, sender=NewStock)
def log_newstock_activity(sender, instance, created, **kwargs):
    """Log when new stock is added."""
    if created:
        ActivityLog.objects.create(
            user=instance.addedByUser,
            actionType='ADD_STOCK',
            description=f"Added {instance.quantity} units of {instance.inventory.product.productName} from {instance.supplier.name if instance.supplier else 'Unknown supplier'}"
        )


# ----- Invoice Activity Logging -----
@receiver(post_save, sender=Invoice)
def log_invoice_activity(sender, instance, created, **kwargs):
    """Log when invoices are created or updated."""
    user = instance.createdByUser
    
    if created:
        ActivityLog.objects.create(
            user=user,
            actionType='CREATE_INVOICE',
            description=f"Created invoice #{instance.invoiceId} for {instance.customer.name if instance.customer else 'Unknown'} - Total: ${instance.grandTotal} - Status: {instance.status}"
        )
    else:
        # Check if status changed
        previous_status = _invoice_previous_status.get(instance.pk)
        if previous_status and previous_status != instance.status:
            ActivityLog.objects.create(
                user=user,
                actionType='UPDATE_INVOICE_STATUS',
                description=f"Invoice #{instance.invoiceId} status changed: {previous_status} → {instance.status}"
            )
        else:
            ActivityLog.objects.create(
                user=user,
                actionType='UPDATE_INVOICE',
                description=f"Updated invoice #{instance.invoiceId}"
            )


@receiver(post_delete, sender=Invoice)
def log_invoice_deletion(sender, instance, **kwargs):
    """Log when invoices are deleted."""
    ActivityLog.objects.create(
        user=instance.createdByUser,
        actionType='DELETE_INVOICE',
        description=f"Deleted invoice #{instance.invoiceId}"
    )


# ----- Customer Activity Logging -----
@receiver(post_save, sender=Customer)
def log_customer_activity(sender, instance, created, **kwargs):
    """Log when customers are created or updated."""
    if created:
        ActivityLog.objects.create(
            user=None,
            actionType='CREATE_CUSTOMER',
            description=f"Created customer: {instance.name} ({instance.customerType})"
        )
    else:
        ActivityLog.objects.create(
            user=None,
            actionType='UPDATE_CUSTOMER',
            description=f"Updated customer: {instance.name}"
        )


@receiver(post_delete, sender=Customer)
def log_customer_deletion(sender, instance, **kwargs):
    """Log when customers are deleted."""
    ActivityLog.objects.create(
        user=None,
        actionType='DELETE_CUSTOMER',
        description=f"Deleted customer: {instance.name}"
    )


# ----- Transaction Activity Logging -----
@receiver(post_save, sender=Transaction)
def log_transaction_activity(sender, instance, created, **kwargs):
    """Log when transactions are created or updated."""
    user = instance.recordedByUser
    
    if created:
        ActivityLog.objects.create(
            user=user,
            actionType='CREATE_TRANSACTION',
            description=f"Recorded transaction #{instance.transactionId} - Invoice #{instance.invoice.invoiceId} - Amount: ${instance.amountPaid} - Method: {instance.paymentMethod} - Status: {instance.transactionStatus}"
        )
    else:
        ActivityLog.objects.create(
            user=user,
            actionType='UPDATE_TRANSACTION',
            description=f"Updated transaction #{instance.transactionId} - Status: {instance.transactionStatus}"
        )


@receiver(post_delete, sender=Transaction)
def log_transaction_deletion(sender, instance, **kwargs):
    """Log when transactions are deleted."""
    ActivityLog.objects.create(
        user=instance.recordedByUser,
        actionType='DELETE_TRANSACTION',
        description=f"Deleted transaction #{instance.transactionId}"
    )


# ----- User Activity Logging -----
@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    """Log when users are created or updated."""
    if created:
        ActivityLog.objects.create(
            user=None,
            actionType='CREATE_USER',
            description=f"Created user: {instance.username} with role: {instance.role}"
        )
    else:
        ActivityLog.objects.create(
            user=instance,
            actionType='UPDATE_USER',
            description=f"Updated user profile: {instance.username}"
        )


@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    """Log when users are deleted."""
    ActivityLog.objects.create(
        user=None,
        actionType='DELETE_USER',
        description=f"Deleted user: {instance.username}"
    )