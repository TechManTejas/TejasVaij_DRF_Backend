from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from user import views as user_views

router = DefaultRouter()
router.register(r"user-info", user_views.UserInfoViewSet, basename="user-info")
router.register(r"visits", user_views.VisitViewSet, basename="visits")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    # User APIs
    path(
        "auth/refresh/",
        user_views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("google-complete/", user_views.google_complete, name="google_complete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
