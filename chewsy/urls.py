from django.contrib import admin
from django.urls import path, include
from recipes.views import (
    HomeView,
    SignupView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('recipes/', include('recipes.urls')),
]
