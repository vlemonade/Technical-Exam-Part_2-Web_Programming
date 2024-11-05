from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import StockViewSet, OrderViewSet, ProfileViewSet

# Create router instances
router = DefaultRouter()
router.register(r'Profile', ProfileViewSet, basename='profile')
router.register(r'Market', StockViewSet, basename='market')
router.register(r'Orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('trading/', include(router.urls)),
]
