# VaultTracker 💳

VaultTracker is a full-stack personal finance and expense tracking application built using Django 6.1 and Tailwind CSS. It enables users to log expenses, manage custom spending categories, and visualize budget progress dynamically in real time.

## Key Features
- **Authentication**: Custom user registration, login, and CSRF-protected POST logout flow.
- **Dynamic Dashboard**: Visual spending summaries and real-time category budget progress bars.
- **Expense Logging**: `ModelForm`-driven expense entry bound to individual authenticated user accounts.
- **Category Management**: Dedicated interface for setting and adjusting monthly target budgets.

## Tech Stack
- **Backend**: Python 3.14, Django 6.1
- **Frontend**: HTML5, Tailwind CSS, Jinja Template Engine
- **Database**: SQLite (Development) / PostgreSQL-ready

## Local Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/](https://github.com/)Charleon01/vault-tracker.git
   cd vault-tracker