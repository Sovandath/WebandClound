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
    # Make password write-only so it won't be exposed in API responses
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'password']

    def create(self, validated_data):
        # Pop the password and create user with hashed password
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password update correctly
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

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