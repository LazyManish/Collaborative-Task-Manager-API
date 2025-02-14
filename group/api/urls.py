from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSets


router = DefaultRouter()
router.register(r'groups',GroupViewSets)


urlpatterns = [
    
    path('', include(router.urls))
]