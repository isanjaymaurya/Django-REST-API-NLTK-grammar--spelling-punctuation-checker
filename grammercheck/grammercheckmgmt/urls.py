from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'check-grammar', views.TextView, 'check-grammar')

urlpatterns = [
    path('check-grammar/', views.TextView.as_view({'post': 'check_grammar'})),
]