"""
Database connection module for PostgreSQL.

This module provides functionality to connect to a PostgreSQL database
using environment variables for configuration.
"""

import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env.local')


class DbConnection:
    """Handles PostgreSQL database connections."""
    
    def __init__(self):
        """Initialize database connection parameters from environment variables."""
        self.db_host = os.getenv('host', 'localhost')
        self.db_port = os.getenv('port', '5432')
        self.db_name = os.getenv('dbname', 'postgres')
        self.db_user = os.getenv('user', 'postgres')
        self.db_password = os.getenv('password', '')
    
    def get_connection(self):
        """
        Get a database connection.
        
        Returns:
            psycopg2.connection: Database connection object
            
        Raises:
            psycopg2.Error: If connection fails
        """
        try:
            connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            return connection
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def test_connection(self):
        """
        Test the database connection.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            if version and len(version) > 0 and version[0] is not None:
                print(f"Connected to PostgreSQL: {version[0]}")
            else:
                print("Connected to PostgreSQL: version information not available")
            return True
        except psycopg2.Error as e:
            print(f"Connection test failed: {e}")
            return False
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


def get_db_connection():
    """
    Convenience function to get a database connection.
    
    Returns:
        psycopg2.connection: Database connection object
    """
    db = DbConnection()
    return db.get_connection()
