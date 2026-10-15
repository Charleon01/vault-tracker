from rest_framework import serializers
# Replace 'Expense' with your actual model name if different (e.g. Vault, Item, etc.)
from .models import Expense 

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__' # Or specify a list of fields like ['id', 'title', 'amount', 'created_at']