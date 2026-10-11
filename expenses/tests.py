from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationSecurityTests(TestCase):
    
    def setUp(self):
        # Create a test user for auth tests
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_dashboard_redirects_unauthenticated_user(self):
        """Ensure unauthenticated users cannot access the dashboard and get redirected to login."""
        response = self.client.get(reverse('dashboard'))
        # Django's login_required decorator redirects with status 302
        self.assertEqual(response.status_code, 302)
        # Check that it redirects to your configured login URL
        self.assertIn('/login/', response.url)

    def test_authenticated_user_can_access_dashboard(self):
        """Ensure logged-in users can successfully access the dashboard."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_renders_successfully(self):
        """Ensure the login page loads correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)