#!/usr/bin/env python3
"""
Database seeding script for PostgreSQL.

This script reads database connection info from .env.local file,
connects to a PostgreSQL database, creates sample tables, and
seeds them with fake data using the Faker library.
"""

from seed.seed import seed_db


def main() -> None:
    """Main function to orchestrate database seeding."""
    print("=" * 60)
    print("PostgreSQL Database Seeding Script")
    print("=" * 60)

    try:
        # Seed database
        seed_db()

        print("=" * 60)
        print("Database seeding completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"An error occurred during database seeding: {e}")


if __name__ == "__main__":
    main()
