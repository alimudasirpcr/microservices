import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from decouple import config
# Function to create a DNS record


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_dns(request):
    """
    Create a CNAME DNS record using the Cloudflare API.
    """
    if request.method == "POST":
        try:
            # Parse tenant_name from the request body
            body = json.loads(request.body)
            tenant_name = body.get('tenant_name')

            if not tenant_name:
                return JsonResponse({'error': 'Tenant name is required.'}, status=400)

            # Cloudflare API credentials
            zone_id = '39721e473aaf9a10f3bf65d48895d816'  # Replace with your Zone ID
            api_token = config('CLOUDFLARE_API_TOKEN')   # Replace with your API token

            # Data for the CNAME record
            data = {
                'type': 'CNAME',
                'name': f'{tenant_name}.oo.om',
                'content': 'ecom-multivendor.omancloud.net',  # Replace with target for CNAME record
                'ttl': 3600,  # Time to live
                'proxied': False  # Set to True to enable proxying
            }

            # Make the API request
            response = requests.post(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                headers={
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json"
                },
                data=json.dumps(data)
            )

            # Return the API response
            return JsonResponse(response.json(), status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
        except requests.RequestException as e:
            return JsonResponse({'error': f'Error connecting to Cloudflare API: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


# Function to get DNS zones
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dns_zones(request):
    """
    Retrieve DNS zones using the Cloudflare API.
    """
    if request.method == "GET":
        try:
#-5d-0Om4W4JofOUFqY7b-moXcKyqRMeFzHaGTend
            # Cloudflare API credentials
            api_token = config('CLOUDFLARE_API_TOKEN')  # Replace with your API token

        
            # Make the API request
            response = requests.get(
                "https://api.cloudflare.com/client/v4/zones",
                headers={
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json"
                }
            )

            # Return the API response
            return JsonResponse(response.json(), status=response.status_code)

        except requests.RequestException as e:
            return JsonResponse({'error': f'Error connecting to Cloudflare API: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)
