from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Маршрути автентифікації вашого варіанта додайте тут: /api/v1/auth/...
    # JWT авторизація
    path("api/v1/auth/jwt/create/", TokenObtainPairView.as_view()),
    path("api/v1/auth/jwt/refresh/", TokenRefreshView.as_view()),
    path("api/v1/auth/jwt/logout/", TokenBlacklistView.as_view()),
    # Основний API
    path("api/v1/", include("bookstore.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
