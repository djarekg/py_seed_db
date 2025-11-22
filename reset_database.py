"""
Database reset script for clearing tables.

This script resets the following tables at the beginning of each run:
- User
- State
- Product
- ProductSale
"""

import sys
from psycopg2 import sql
from db_connection import DatabaseConnection


def reset_tables():
    """
    Reset (truncate) database tables: User, State, Product, ProductSale.
    
    This function will:
    1. Connect to the database
    2. Truncate each table with CASCADE to handle foreign key constraints
    3. Reset sequences for auto-incrementing primary keys
    
    Returns:
        bool: True if reset is successful, False otherwise
    """
    db = DatabaseConnection()
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        print("Starting database reset...")
        
        # List of tables to reset
        tables = ['User', 'State', 'Product', 'ProductSale']
        
        # Truncate tables with CASCADE to handle foreign key constraints
        # Note: TRUNCATE is a DDL statement that auto-commits in PostgreSQL
        success_count = 0
        for table in tables:
            try:
                print(f"Resetting table: {table}")
                # TRUNCATE removes all rows and resets sequences
                # CASCADE automatically truncates dependent tables
                # RESTART IDENTITY resets auto-increment sequences
                # Using sql.Identifier to safely handle table names
                query = sql.SQL('TRUNCATE TABLE {} RESTART IDENTITY CASCADE;').format(
                    sql.Identifier(table)
                )
                cursor.execute(query)
                conn.commit()  # Commit each table individually
                success_count += 1
                print(f"✓ Table {table} reset successfully")
            except Exception as e:
                print(f"✗ Error resetting table {table}: {e}")
                # Continue with other tables even if one fails
                conn.rollback()
                continue
        
        print(f"\nDatabase reset completed! {success_count}/{len(tables)} tables reset successfully.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\nError during database reset: {e}")
        if 'conn' in locals():
            conn.close()
        return False


def main():
    """Main function to execute database reset."""
    print("=" * 60)
    print("DATABASE RESET UTILITY")
    print("=" * 60)
    print("\nThis will reset the following tables:")
    print("  - User")
    print("  - State")
    print("  - Product")
    print("  - ProductSale")
    print("\nAll data in these tables will be PERMANENTLY deleted!")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Database reset cancelled.")
        sys.exit(0)
    
    print()
    success = reset_tables()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
