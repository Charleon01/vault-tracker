from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet


router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
]



