"""
Database connection module for PostgreSQL.

This module provides functionality to connect to a PostgreSQL database
using environment variables for configuration.
"""

import os
import psycopg2
from psycopg2 import pool
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConnection:
    """Handles PostgreSQL database connections."""
    
    def __init__(self):
        """Initialize database connection parameters from environment variables."""
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'postgres')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', '')
        self.connection_pool: Optional[psycopg2.pool.SimpleConnectionPool] = None
    
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
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Connected to PostgreSQL: {version[0]}")
            cursor.close()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"Connection test failed: {e}")
            return False


def get_db_connection():
    """
    Convenience function to get a database connection.
    
    Returns:
        psycopg2.connection: Database connection object
    """
    db = DatabaseConnection()
    return db.get_connection()
