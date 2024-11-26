import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Tenant
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from decouple import config

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_tenant(request):
    """
    Create a tenant by making an external API request and store tenant information in the database.
    """
    if request.method == "POST":
        # Parse tenant_name from the request body
        body = json.loads(request.body)
        tenant_name = body.get('tenant_name')

        if not tenant_name:
            return JsonResponse({'error': 'Tenant name is required.'}, status=400)

        # API Key and URL for the external service
        api_key = config('SERVER_API_KEY')
        api_url = config('SERVER_URL')

        # Data to send to the external API
        data = {
            "key": api_key,
            "action": "add",
            "domain": f"{tenant_name}.oo.om",  # Tenant domain
            "user": tenant_name,  # Tenant username
            "pass": "PASSWORD",  # Replace with a secure password
            "email": f"{tenant_name}@account",  # Tenant email
            "package": "1",  # Package ID
            "inode": "0",
            "limit_nproc": "40",
            "limit_nofile": "0",
            "debug": 1,
            "server_ips": "65.109.95.216"
        }

        try:
            # Make the POST request to the external API
            response = requests.post(api_url, data=data, verify=False)
            response_data = response.json()

            # Check the response from the external API
            if response.status_code == 200 and response_data.get('status') == "OK":
                # Save tenant information to the database
                tenant = Tenant.objects.create(
                    name=tenant_name,
                    domain=f"{tenant_name}.oo.om",
                    email=f"{tenant_name}@account"
                )
                return JsonResponse({
                    'message': 'Account created successfully!',
                    'tenant': {
                        'id': tenant.id,
                        'name': tenant.name,
                        'domain': tenant.domain,
                        'email': tenant.email
                    }
                }, status=200)
            else:
                return JsonResponse({'error': response_data.get('message', 'Failed to create account')}, status=400)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Error connecting to API: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tenants(request):
    """
    List all tenants stored in the database.
    """
    if request.method == "GET":
        tenants = Tenant.objects.all().values('id', 'name', 'domain', 'email', 'created_at')
        return JsonResponse({'tenants': list(tenants)}, status=200)

    return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tenant(request, tenant_id):
    """
    Retrieve details of a specific tenant by ID.
    """
    if request.method == "GET":
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            return JsonResponse({
                'tenant': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'domain': tenant.domain,
                    'email': tenant.email,
                    'created_at': tenant.created_at
                }
            }, status=200)
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Tenant not found.'}, status=404)

    return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_tenant(request, tenant_id):
    """
    Delete a tenant from the database by ID.
    """
    if request.method == "DELETE":
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            tenant.delete()
            return JsonResponse({'message': 'Tenant deleted successfully.'}, status=200)
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Tenant not found.'}, status=404)

    return JsonResponse({'error': 'Only DELETE requests are allowed.'}, status=405)
