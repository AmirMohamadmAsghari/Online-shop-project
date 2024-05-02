from django.urls import path
from .views import Home_View
urlpatterns = [
    path('', Home_View.as_view(), name='home'),
]