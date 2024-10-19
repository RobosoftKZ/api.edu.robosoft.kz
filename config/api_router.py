from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from apps.users.api.views import UserViewSet, UsernameCheckerAPIView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
# router.register("")


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("testing/", include("apps.subjects.urls")),
    path('check-username/', UsernameCheckerAPIView.as_view(), name='check-username'),

]
