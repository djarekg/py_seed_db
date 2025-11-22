# py_seed_db
Seed Postgres database with Python

A Python project that seeds a PostgreSQL database with fake data using Faker library.

## Features

- Uses `venv` for virtual environment management
- Manages dependencies with `pip` and `requirements.txt`
- Reads database connection info from `.env.local` file
- Generates fake data using the Faker library
- Seeds PostgreSQL database with sample users and products
- Includes code linting with Ruff

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (running locally or remotely)
- pip package manager

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/djarekg/py_seed_db.git
cd py_seed_db
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Linux/macOS:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure database connection

Copy the example environment file and update with your database credentials:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set your PostgreSQL connection details:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seeddb
DB_USER=postgres
DB_PASSWORD=your_password_here
```

**Note:** Make sure the database specified in `DB_NAME` already exists. You can create it with:
```bash
createdb seeddb
```
or via psql:
```sql
CREATE DATABASE seeddb;
```

## Usage

### Run the seeding script

With the virtual environment activated:

```bash
python seed_db.py
```

This will:
1. Connect to your PostgreSQL database using credentials from `.env.local`
2. Create two tables: `users` and `products` (if they don't exist)
3. Seed the `users` table with 50 fake user records
4. Seed the `products` table with 100 fake product records

### Lint the code

You can lint the Python code using Ruff:

```bash
ruff check .
```

To automatically fix linting issues:

```bash
ruff check --fix .
```

## Project Structure

```
py_seed_db/
├── .env.local.example    # Example environment configuration
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── seed_db.py          # Main seeding script
```

## Dependencies

- **Faker** (30.8.2): Library for generating fake data
- **python-dotenv** (1.0.1): Reads key-value pairs from `.env.local` file
- **psycopg2-binary** (2.9.10): PostgreSQL adapter for Python
- **ruff** (0.8.2): Fast Python linter

## Database Schema

### Users Table
- `id` (SERIAL PRIMARY KEY)
- `first_name` (VARCHAR)
- `last_name` (VARCHAR)
- `email` (VARCHAR, UNIQUE)
- `phone` (VARCHAR)
- `address` (TEXT)
- `city` (VARCHAR)
- `country` (VARCHAR)
- `created_at` (TIMESTAMP)

### Products Table
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR)
- `description` (TEXT)
- `price` (DECIMAL)
- `category` (VARCHAR)
- `created_at` (TIMESTAMP)

## Security Notes

- Never commit your `.env.local` file to version control (it's already in `.gitignore`)
- Use strong passwords for your database
- Consider using environment-specific configuration files for different deployment environments

## License

See LICENSE file for details.
