from django.urls import path
from .views import regenerate_token

urlpatterns = [
    path('regenerate-token/', regenerate_token, name='regenerate_token'),
]