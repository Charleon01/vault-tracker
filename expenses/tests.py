from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from expenses.models import Category, Expense
from rest_framework.test import APITestCase
from rest_framework import status


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

class ExpenseAPITests(APITestCase):
    def setUp(self):
        # Create a test user, category, and sample expense matching your model schema
        self.user = User.objects.create_user(username='apitestuser', password='password123')
        self.category = Category.objects.create(
            user=self.user,
            name="Utilities",
            type="expense",
            monthly_budget=300.00
        )
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=45.00,
            date=date.today(),
            note='Test Groceries'
        )
        
    def test_get_expenses_list(self):
        """Ensure we can retrieve the list of expenses via API."""
        url = reverse('expense-list')  # Assumes router registration basename/name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['note'], 'Test Groceries')

    def test_create_expense_authenticated(self):
        """Ensure an authenticated user can successfully create a new expense (POST request)."""
        self.client.login(username='apitestuser', password='password123')
        url = reverse('expense-list')
        data = {
            'user': self.user.id,  # Include the user ID here
            'category': self.category.id,
            'amount': 15.00,
            'date': str(date.today()),
            'note': 'Transport'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)