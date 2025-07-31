"""
Database connection utilities for Crafty CRM.

Simple utilities for connecting to PostgreSQL database for running
scripts and queries using psycopg for raw SQL.
"""

import os
import psycopg
import pandas as pd
from psycopg.rows import dict_row


class Database:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.user = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DB", "crafty")
        self._connection = None

    @property
    def connection_string(self):
        """Get PostgreSQL connection string."""
        return f"host={self.host} port={self.port} user={self.user} password={self.password} dbname={self.database}"

    def get_connection(self):
        """Get psycopg connection."""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg.connect(
                self.connection_string, row_factory=dict_row
            )
        return self._connection

    def close_connection(self):
        """Close the database connection."""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, params: dict = None) -> dict:
        """Execute SQL query and return raw results as dictionary."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or {})
                result = cursor.fetchone()
                return result if result else {}
        finally:
            conn.close()

    def execute_insert(self, query: str, params: dict = None) -> bool:
        """Execute INSERT query and return success status."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or {})
                conn.commit()
                return True
        except Exception as e:
            print(f"Insert failed: {e}")
            return False
        finally:
            conn.close()

    def execute_query_df(self, query: str, params: dict = None) -> pd.DataFrame:
        """Execute SQL query and return results as a pandas DataFrame."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or {})
                return pd.DataFrame(cursor.fetchall())
        finally:
            conn.close()

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
                print("Database connection successful!")
                return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
        finally:
            if conn:
                conn.close()
