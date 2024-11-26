from django.urls import path
from .views import create_tenant, list_tenants, get_tenant, delete_tenant

urlpatterns = [
    path('create-tenant/', create_tenant, name='create_tenant'),  # POST: Create a tenant
    path('tenants/', list_tenants, name='list_tenants'),         # GET: List all tenants
    path('tenants/<int:tenant_id>/', get_tenant, name='get_tenant'),  # GET: Retrieve a specific tenant
    path('tenants/<int:tenant_id>/delete/', delete_tenant, name='delete_tenant'),  # DELETE: Delete a tenant
]