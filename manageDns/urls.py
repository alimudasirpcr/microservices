from django.urls import path
from .views import create_dns, get_dns_zones

urlpatterns = [
    path('create-dns/', create_dns, name='create_dns'),  # POST: Create DNS record
    path('get-dns-zones/', get_dns_zones, name='get_dns_zones'),  # GET: Retrieve DNS zones
]