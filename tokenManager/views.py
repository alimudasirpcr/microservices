from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@api_view(['POST'])
@authentication_classes([])  # Disable authentication
@permission_classes([])      # Disable permission requirements
def regenerate_token(request):
    """
    Regenerate a token for a user based on their username and password.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)

    try:
        # Authenticate the user
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=401)

        # Delete any existing token for the user
        Token.objects.filter(user=user).delete()

        # Create a new token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=200)

    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)
