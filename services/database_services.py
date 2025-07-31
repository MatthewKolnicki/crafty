"""
Database services.

This module contains business logic for database operations,
including query execution and data processing.
"""

from typing import Dict, Any, Optional
from connectors.database import Database


class DatabaseService:
    """Service class for database operations."""

    def __init__(self):
        self.db = Database()

    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a SQL query and return results.

        Args:
            query: SQL query to execute
            params: Optional parameters for the query

        Returns:
            Query results as dictionary
        """
        return self.db.execute_query(query, params)

    def execute_insert(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Execute an INSERT query.

        Args:
            query: SQL INSERT query to execute
            params: Optional parameters for the query

        Returns:
            Success status
        """
        return self.db.execute_insert(query, params)

    def execute_query_df(self, query: str, params: Optional[Dict[str, Any]] = None):
        """
        Execute a SQL query and return results as DataFrame.

        Args:
            query: SQL query to execute
            params: Optional parameters for the query

        Returns:
            Query results as pandas DataFrame
        """
        return self.db.execute_query_df(query, params)

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            Connection status
        """
        return self.db.test_connection()

    def close_connection(self):
        """Close the database connection."""
        self.db.close_connection()
