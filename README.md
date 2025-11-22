# py_seed_db
Seed Postgres database with Python

## Overview

This project provides Python scripts for connecting to a PostgreSQL database and managing database tables for seeding purposes.

## Features

- **Database Connection Module** (`db_connection.py`): Handles PostgreSQL connections using environment variables
- **Database Reset Script** (`reset_database.py`): Resets tables (User, State, Product, ProductSale) at the beginning of each run

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database Connection**
   
   Copy the example environment file and update with your database credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database details:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

## Usage

### Database Connection

Use the `db_connection.py` module to connect to your database:

```python
from db_connection import DatabaseConnection, get_db_connection

# Method 1: Using DatabaseConnection class
db = DatabaseConnection()
conn = db.get_connection()

# Method 2: Using convenience function
conn = get_db_connection()

# Test connection
db = DatabaseConnection()
db.test_connection()
```

### Reset Database Tables

Run the reset script to clear all data from User, State, Product, and ProductSale tables:

```bash
python reset_database.py
```

**Warning**: This will permanently delete all data in the specified tables!

## Database Tables

The reset script manages the following tables:
- `User`
- `State`
- `Product`
- `ProductSale`

## Requirements

- Python 3.7+
- PostgreSQL database
- psycopg2-binary
- python-dotenv
