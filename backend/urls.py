from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import CategoryView, ShopView, ContactView

router = DefaultRouter()
router.register('user/contact', ContactView, basename='contact')



app_name = 'backend'
urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('categories', CategoryView.as_view(), name='categories'),
    path('shops', ShopView.as_view(), name='shops'),
] + router.urls
