"""
SQL Query services.

This module contains business logic for SQL query operations,
including complex analytics queries and data processing.
"""

from typing import Dict, Any
from services.database_services import DatabaseService


class SQLQueryService:
    """Service class for SQL query operations."""

    def __init__(self):
        self.db_service = DatabaseService()

    def get_engagement_counts_by_company(self) -> Dict[str, Any]:
        """
        Get engagement counts by company for the last 30 days.

        Returns:
            Dictionary with results containing companies and their engagement counts
        """
        query = """
        SELECT
            ce.Company_id,
            COUNT(DISTINCT ce.Engagement_id) AS engagements_last_month
        FROM 
            client_engagements ce
        WHERE
            ce.Timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
        GROUP BY
            ce.Company_id;
        """
        try:
            results = self.db_service.execute_query_df(query)
            return {"results": results.to_dict(orient="records")}
        finally:
            self.db_service.close_connection()

    def get_average_resolution_time_by_company(self) -> Dict[str, Any]:
        """
        Get average resolution time by company for closed tickets.

        Returns:
            Dictionary with results containing companies and their average resolution times
        """
        query = """
        SELECT
            st.company_id,
            ROUND(AVG(EXTRACT(EPOCH FROM (st.closed_at::timestamp - st.created_at::timestamp)))) AS avg_resolution_time_seconds
        FROM 
            support_tickets st
        WHERE
            st.status = 'Closed'
            AND st.closed_at IS NOT NULL
        GROUP BY
            st.company_id;
        """
        try:
            results = self.db_service.execute_query_df(query)
            return {"results": results.to_dict(orient="records")}
        finally:
            self.db_service.close_connection()

    def get_ticket_counts_by_engagement_bucket(self) -> Dict[str, Any]:
        """
        Get ticket counts by engagement bucket (high/medium/low).

        Returns:
            Dictionary with results containing ticket counts grouped by engagement level buckets
        """
        query = """
        WITH company_buckets AS (
            SELECT
                engagement.company_id,
                /*
                this calculates the engagement count twice, it simplifies the query but
                I could separate this into another CTE to avoid the unnecessary compute
                */
                CASE
                    WHEN COUNT(engagement.engagement_id) > 10 THEN 'high'
                    WHEN COUNT(engagement.engagement_id) BETWEEN 3 AND 10 THEN 'medium'
                    ELSE 'low'
                END AS bucket,
                COUNT(ticket.ticket_id) AS ticket_count
            FROM
                client_engagements engagement
            JOIN 
                support_tickets ticket
            USING(company_id)
            WHERE 
                engagement.Timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
            GROUP BY
                engagement.company_id
        )
        SELECT
            company_buckets.bucket,
            SUM(company_buckets.ticket_count) AS ticket_count
        FROM
            company_buckets
        GROUP BY
            company_buckets.bucket;
        """
        try:
            results = self.db_service.execute_query_df(query)
            return {"results": results.to_dict(orient="records")}
        finally:
            self.db_service.close_connection()

    def get_ticket_counts_by_engagement_bucket_alternative(self) -> Dict[str, Any]:
        """
        Get ticket counts by engagement bucket (high/medium/low) using rolling window approach.

        Returns:
            Dictionary with results containing ticket counts grouped by engagement level buckets
        """
        query = """
        WITH rolling_window_stats AS (
            SELECT DISTINCT
                e1.Company_id,
                e1.Timestamp as window_start,
                COUNT(e2.Engagement_id) as engagements_in_window
            FROM 
                client_engagements e1
            JOIN 
                client_engagements e2 
                ON e1.Company_id = e2.Company_id
                AND e2.Timestamp >= e1.Timestamp 
                AND e2.Timestamp <= e1.Timestamp + INTERVAL '30 days'
            GROUP BY 
                e1.Company_id, e1.Timestamp
        ),
        company_max_window_activity AS (
            SELECT
                Company_id,
                MAX(engagements_in_window) AS max_engagements_in_any_window
            FROM
                rolling_window_stats
            GROUP BY
                Company_id
        ),
        company_buckets AS (
            SELECT
                Company_id,
                CASE
                    WHEN max_engagements_in_any_window > 10 THEN 'high'
                    WHEN max_engagements_in_any_window BETWEEN 3 AND 10 THEN 'medium'
                    ELSE 'low'
                END AS bucket
            FROM
                company_max_window_activity
        )
        SELECT
            cb.bucket,
            COUNT(st.ticket_id) AS open_ticket_count
        FROM
            company_buckets cb
        JOIN
            support_tickets st
        USING(company_id)
        WHERE
            st.status = 'Open'
        GROUP BY
            cb.bucket;
        """
        try:
            results = self.db_service.execute_query_df(query)
            return {"results": results.to_dict(orient="records")}
        finally:
            self.db_service.close_connection() 