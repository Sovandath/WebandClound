from rest_framework import serializers
from .models import (
    User,
    Product, 
    Inventory, 
    Category, 
    SubCategory, 
    Source,
    NewStock,
    Customer,
    Invoice,
    Purchase,
    Transaction,
    ActivityLog
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryId', 'name', 'description', 'slug', 'createdAt']
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategoryId', 'category', 'name', 'description', 'createdAt']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['sourceId', 'name', 'sourceUrl', 'contactPerson', 'phone', 'email', 'address', 'createdAt']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'productName', 'description', 'image', 'skuCode', 'unit', 'status', 'subcategory', 'source', 'createdAt']

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['inventoryId', 'product', 'quantity', 'costPrice', 'reorderLevel', 'location', 'updatedAt']

class NewStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewStock
        fields = ['newstockId', 'inventory', 'quantity', 'purchasePrice', 'receivedDate', 'supplier', 'addedByUser', 'note', 'createdAt']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerId', 'name', 'businessAddress', 'phone', 'email', 'customerType', 'firstPurchaseDate', 'createdAt']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoiceId', 'customer', 'createdByUser', 'totalBeforeDiscount', 'discount', 'tax', 'grandTotal', 'paymentMethod', 'invoiceDate', 'note', 'status', 'qrReference', 'createdAt']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['purchaseId', 'invoice', 'product', 'quantity', 'pricePerUnit', 'discount', 'subtotal', 'createdAt']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transactionId', 'invoice', 'customer', 'amountPaid', 'paymentMethod', 'transactionStatus', 'paymentReference', 'transactionDate', 'recordedByUser']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['logId', 'user', 'actionType', 'description', 'createdAt']