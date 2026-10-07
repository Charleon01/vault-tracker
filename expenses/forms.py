from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'note']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'note': forms.Textarea(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'What was this expense for?'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'monthly_budget']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'e.g. Groceries, Rent, Utilities'
            }),
            'monthly_budget': forms.NumberInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'e.g. 600.00',
                'step': '0.01'
            }),
        }


# Keep your existing ExpenseForm and CategoryForm above this...

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'you@example.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password', 'password2']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                })







