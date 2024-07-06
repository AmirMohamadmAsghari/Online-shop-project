from django.urls import path
from .views import Home_View, set_language

urlpatterns = [
    path('', Home_View.as_view(), name='home'),
    path('set_language/', set_language, name='set_language'),
]
