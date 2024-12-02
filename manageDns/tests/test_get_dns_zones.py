import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestGetDNSZonesAPI:
    def setup_method(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('get_dns_zones')  # Replace with your URL name

    @patch('manageDns.views.requests.get')  # Mock the external API call
    def test_get_dns_zones_success(self, mock_get):
        """Test case for a successful response from the external API."""
        mock_response_data = {
            "success": True,
            "result": [
                {"id": "zone1", "name": "example1.com"},
                {"id": "zone2", "name": "example2.com"}
            ]
        }
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True
        assert len(response.json()["result"]) == 2

    @patch('manageDns.views.requests.get')  # Mock the external API call
    def test_get_dns_zones_api_error(self, mock_get):
        """Test case for an error response from the external API."""
        mock_response_data = {"success": False, "errors": [{"message": "API error"}]}
        mock_get.return_value.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_get.return_value.json.return_value = mock_response_data

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["success"] is False
        assert "errors" in response.json()

    def test_get_dns_zones_unauthorized(self):
        """Test case for unauthorized access without a token."""
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()
        assert response.json()["detail"] == "Authentication credentials were not provided."

    def test_get_dns_zones_missing_token(self):
        # Test with a missing token
        self.client.credentials()  # Clear any existing credentials
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credentials" in response.json()["detail"]

    def test_get_dns_zones_with_invalid_token(self):
        # Test with an invalid token
        self.client.credentials(HTTP_AUTHORIZATION="Token INVALID_TOKEN")
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid" in response.json()["detail"]

    @patch("manageDns.views.requests.get")
    def test_get_dns_zones_with_empty_response(self, mock_get):
        # Simulate an empty API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"success": True, "result": []}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["result"] == []
