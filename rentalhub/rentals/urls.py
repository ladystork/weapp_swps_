from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RentalViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
