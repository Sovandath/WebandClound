from django.db import models

# Reusable role choices for User model
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Cashier', 'Cashier'),
]

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    passwordHash = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    googleId = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    subcategoryId = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} → {self.category.name}"
    
class Source(models.Model):
    sourceId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Supplier or origin name
    sourceUrl = models.URLField(max_length=500, null=True, blank=True)  # Website or contact link
    contactPerson = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
# Reusable status choices for product availability
STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Discontinued', 'Discontinued'),
]

class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=500, null=True, blank=True)  # URL or path to image
    skuCode = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)  # e.g., pcs, box, kg
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='products')
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.productName} ({self.skuCode})"


class Inventory(models.Model):
    inventoryId = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='inventory_records')
    quantity = models.IntegerField()
    costPrice = models.DecimalField(max_digits=10, decimal_places=2)
    reorderLevel = models.IntegerField()
    location = models.CharField(max_length=255)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.productName} @ {self.location} — {self.quantity} units"


class NewStock(models.Model):
    newstockId = models.AutoField(primary_key=True)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name='stock_entries')
    quantity = models.IntegerField()
    purchasePrice = models.DecimalField(max_digits=10, decimal_places=2)
    receivedDate = models.DateField()
    supplier = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_supplied')
    addedByUser = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_added')
    note = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock +{self.quantity} → {self.inventory.product.productName} on {self.receivedDate}"
    
# Reusable customer type choices
CUSTOMER_TYPE_CHOICES = [
    ('Individual', 'Individual'),
    ('Business', 'Business'),
]

class Customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    businessAddress = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    customerType = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES)
    firstPurchaseDate = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.customerType})"


# Reusable enums for payment method and invoice status
PAYMENT_METHOD_CHOICES = [
    ('Cash', 'Cash'),
    ('Card', 'Card'),
    ('KHQR', 'KHQR'),
    ('BankTransfer', 'BankTransfer'),
    ('Other', 'Other'),
]

INVOICE_STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),
    ('Cancelled', 'Cancelled'),
]

class Invoice(models.Model):
    invoiceId = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, related_name='invoices')
    createdByUser = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='invoices_created')
    totalBeforeDiscount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grandTotal = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    invoiceDate = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, default='Draft')
    qrReference = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoiceId} — {self.status}"


class Purchase(models.Model):
    purchaseId = models.AutoField(primary_key=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    quantity = models.IntegerField()
    pricePerUnit = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} × {self.product.productName if self.product else 'Unknown'} → Invoice #{self.invoice.invoiceId}"
    
# Reusable enums for payment method and transaction status
TRANSACTION_METHOD_CHOICES = [
    ('Cash', 'Cash'),
    ('Card', 'Card'),
    ('KHQR', 'KHQR'),
    ('BankTransfer', 'BankTransfer'),
    ('Other', 'Other'),
]

TRANSACTION_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('Refunded', 'Refunded'),
]

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, related_name='transactions')
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=20, choices=TRANSACTION_METHOD_CHOICES)
    transactionStatus = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES)
    paymentReference = models.CharField(max_length=255, null=True, blank=True)
    transactionDate = models.DateTimeField()
    recordedByUser = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='transactions_recorded')

    def __str__(self):
        return f"Txn #{self.transactionId} — {self.transactionStatus} ({self.amountPaid})"
    
class ActivityLog(models.Model):
    logId = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    actionType = models.CharField(max_length=100)  # e.g., 'ADD_PRODUCT', 'DELETE_INVOICE'
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actionType} by {self.user.name if self.user else 'Unknown'}"