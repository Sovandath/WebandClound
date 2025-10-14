from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # Grappelli admin
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
