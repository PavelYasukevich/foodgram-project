from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    
]
