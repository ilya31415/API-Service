from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import CategoryView, ShopView, ContactView, PartnerUpdate, ProductInfoView, PartnerStateView, \
    BasketView, PartnerOrders, OrderView

http_method = {"delete": "destroy",
               "post": "create",
               "put": "partial_update",
               "get": "retrieve"}

app_name = 'backend'

router = DefaultRouter()
router.register('products', ProductInfoView)
# router.register('order', OrderView, basename='order')

urlpatterns = [
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.authtoken')),
                  path('categories', CategoryView.as_view(), name='categories'),
                  path('shops', ShopView.as_view(), name='shops'),
                  path('user/contact/', ContactView.as_view(http_method), name='contact'),
                  path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
                  path('partner/state', PartnerStateView.as_view({"put": "partial_update",
                                                                  "get": "retrieve"}), name='partner-state'),
                  path('basket/', BasketView.as_view(http_method), name='contact'),
                  path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
                  path('order', OrderView.as_view({"put": "partial_update",
                                                                  "get": "list"}), name='order'),

              ] + router.urls
