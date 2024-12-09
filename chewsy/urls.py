from django.contrib import admin
from django.urls import path, include
from recipes.urls import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('recipes/', include('recipes.urls')),
]
