from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # Grappelli admin
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
