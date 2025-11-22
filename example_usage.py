"""
Example usage of the database connection and reset modules.

This script demonstrates how to use the db_connection and reset_database modules.
Note: This requires a running PostgreSQL database with proper credentials in .env file.
"""

from db_connection import DatabaseConnection, get_db_connection


def example_connection_test():
    """Example: Test database connection."""
    print("=" * 60)
    print("Example 1: Testing Database Connection")
    print("=" * 60)
    
    db = DatabaseConnection()
    print(f"\nAttempting to connect to database...")
    print(f"  Host: {db.db_host}")
    print(f"  Port: {db.db_port}")
    print(f"  Database: {db.db_name}")
    # Note: User and password are not displayed for security reasons
    print()
    
    # Test the connection
    success = db.test_connection()
    
    if success:
        print("\n✓ Connection test successful!")
    else:
        print("\n✗ Connection test failed!")
        print("Please check your .env file and database configuration.")


def example_query():
    """Example: Execute a simple query."""
    print("\n" + "=" * 60)
    print("Example 2: Executing a Simple Query")
    print("=" * 60)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT current_database(), current_user;")
        result = cursor.fetchone()
        
        print(f"\nCurrent Database: {result[0]}")
        print(f"Current User: {result[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Query executed successfully!")
        
    except Exception as e:
        print(f"\n✗ Query failed: {e}")


def main():
    """Main function to run examples."""
    print("\n" + "=" * 60)
    print("DATABASE CONNECTION EXAMPLES")
    print("=" * 60)
    print("\nNote: These examples require a running PostgreSQL database")
    print("with credentials configured in the .env file.")
    print("=" * 60 + "\n")
    
    try:
        example_connection_test()
        example_query()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("  1. A running PostgreSQL database")
        print("  2. A .env file with correct credentials")
        print("  3. Installed requirements: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
