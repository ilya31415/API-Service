from django.urls import path, include

app_name = 'backend'
urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
