#!/usr/bin/env python3
"""
Database seeding script for PostgreSQL.

This script reads database connection info from .env.local file,
connects to a PostgreSQL database, creates sample tables, and
seeds them with fake data using the Faker library.
"""

import os
import sys
from typing import Any

import psycopg2
from dotenv import load_dotenv
from faker import Faker

# Initialize Faker
fake = Faker()


def load_env_config() -> dict[str, Any]:
    """Load database configuration from .env.local file."""
    env_path = os.path.join(os.path.dirname(__file__), ".env.local")

    if not os.path.exists(env_path):
        print(f"Error: .env.local file not found at {env_path}")
        print("Please create a .env.local file based on .env.local.example")
        sys.exit(1)

    load_dotenv(env_path)

    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "seeddb"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
    }

    return config


def create_connection(config: dict[str, Any]) -> psycopg2.extensions.connection:
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
        )
        print(
            f"Successfully connected to database '{config['database']}' at {config['host']}:{config['port']}"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """Create sample tables in the database."""
    cursor = conn.cursor()

    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                city VARCHAR(100),
                country VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        print("Tables created successfully")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        sys.exit(1)
    finally:
        cursor.close()


def seed_users(conn: psycopg2.extensions.connection, count: int = 50) -> None:
    """Seed the users table with fake data."""
    cursor = conn.cursor()

    try:
        print(f"Seeding {count} users...")
        
        # Clear unique cache to avoid exhausting unique values
        fake.unique.clear()

        for _ in range(count):
            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, email, phone, address, city, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    fake.first_name(),
                    fake.last_name(),
                    fake.unique.email(),
                    fake.phone_number(),
                    fake.street_address(),
                    fake.city(),
                    fake.country(),
                ),
            )

        conn.commit()
        print(f"Successfully seeded {count} users")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error seeding users: {e}")
    finally:
        cursor.close()


def seed_products(conn: psycopg2.extensions.connection, count: int = 100) -> None:
    """Seed the products table with fake data."""
    cursor = conn.cursor()

    categories = [
        "Electronics",
        "Clothing",
        "Food",
        "Books",
        "Home & Garden",
        "Toys",
        "Sports",
        "Beauty",
        "Automotive",
        "Health",
    ]

    try:
        print(f"Seeding {count} products...")

        for _ in range(count):
            cursor.execute(
                """
                INSERT INTO products (name, description, price, category)
                VALUES (%s, %s, %s, %s)
            """,
                (
                    fake.catch_phrase(),
                    fake.text(max_nb_chars=200),
                    fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=5, max_value=999),
                    fake.random_element(categories),
                ),
            )

        conn.commit()
        print(f"Successfully seeded {count} products")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error seeding products: {e}")
    finally:
        cursor.close()


def main() -> None:
    """Main function to orchestrate database seeding."""
    print("=" * 60)
    print("PostgreSQL Database Seeding Script")
    print("=" * 60)

    # Load configuration
    config = load_env_config()

    # Create database connection
    conn = create_connection(config)

    try:
        # Create tables
        create_tables(conn)

        # Seed data
        seed_users(conn, count=50)
        seed_products(conn, count=100)

        print("=" * 60)
        print("Database seeding completed successfully!")
        print("=" * 60)

    finally:
        conn.close()
        print("Database connection closed")


if __name__ == "__main__":
    main()
