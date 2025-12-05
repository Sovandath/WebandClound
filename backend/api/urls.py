from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router automatically create the url or api endpoint for all methods
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)
router.register(r'sources', views.SourceViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'newstock', views.NewStockViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'activitylogs', views.ActivityLogViewSet)

from .authentication import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]