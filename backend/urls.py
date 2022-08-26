from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import CategoryView, ShopView, ContactView, PartnerUpdate, ProductInfoView

http_method = {"delete": "destroy",
               "post": "create",
               "put": "partial_update",
               "get": "retrieve"}

app_name = 'backend'

router = DefaultRouter()
router.register('products', ProductInfoView)

urlpatterns = [
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.authtoken')),
                  path('categories', CategoryView.as_view(), name='categories'),
                  path('shops', ShopView.as_view(), name='shops'),
                  path('user/contact/', ContactView.as_view(http_method), name='contact'),
                  path('partner/update', PartnerUpdate.as_view(), name='partner-update'),

              ] + router.urls
