from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from expenses.models import Category, Expense

class AuthenticationSecurityTests(TestCase):
    
    def setUp(self):
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_dashboard_redirects_unauthenticated_user(self):
        """Ensure unauthenticated users cannot access the dashboard and get redirected to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
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


class ExpenseModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="financetest", password="password123")
        self.category = Category.objects.create(
            user=self.user,
            name="Food",
            type="expense",
            monthly_budget=500.00
        )

    def test_expense_creation(self):
        """Ensure an expense object can be successfully created and linked to a user and category."""
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=150.00,
            date=date.today(),
            note="Grocery shopping"
        )
        self.assertEqual(float(expense.amount), 150.00)
        self.assertEqual(expense.note, "Grocery shopping")
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.category, self.category)