from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .permissions import (
    IsAdmin,
    IsManager,
    IsStaff,
    IsAdminOrManager,
    IsManagerOrReadOnly
)
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
from .serializers import (
    UserSerializer,
    ProductSerializer, 
    InventorySerializer, 
    CategorySerializer, 
    SubCategorySerializer, 
    SourceSerializer,
    NewStockSerializer,
    CustomerSerializer,
    InvoiceSerializer,
    PurchaseNestedSerializer,
    TransactionSerializer,
    ActivityLogSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin] # Only administrators should manage users

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] # Admins/Managers can manage categories
    
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] # Admins/Managers can manage subcategories

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] # Admins/Managers can manage sources

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can create/edit, Staff can view

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can adjust, Staff can view

class NewStockViewSet(viewsets.ModelViewSet):
    queryset = NewStock.objects.all()
    serializer_class = NewStockSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] # Only Managers/Admins should add new stock
    
    @transaction.atomic 
    def perform_create(self, serializer):
        try:
            new_stock_quantity = serializer.validated_data['quantity']
            inventory_item = serializer.validated_data['inventory']
            
            # Validate quantity is positive
            if new_stock_quantity <= 0:
                raise ValidationError("Stock quantity must be positive")
            
            inventory_item.quantity += new_stock_quantity
            inventory_item.save()
            
            serializer.save()
        except Exception as e:
            raise ValidationError(f"Failed to add stock: {str(e)}")

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can manage customers, Staff can view

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can create/manage invoices, Staff can view

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseNestedSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can create/manage purchases, Staff can view

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly] # Managers/Admins can manage transactions, Staff can view

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager] # Only Managers/Admins should view activity logs