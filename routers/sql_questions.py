from fastapi import APIRouter
from services.database_services import DatabaseService
import pandas as pd

router = APIRouter(prefix="/sql")


@router.get("/question_one")
def get_question_one():
    """
    Question One: Get engagement counts by company for the last 30 days.
    
    Returns:
        List of companies with their engagement counts for the last 30 days
    """
    db_service = DatabaseService()
    try:
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
        results = db_service.execute_query_df(query)
        return {"results": results.to_dict(orient="records")}
    finally:
        db_service.close_connection()


@router.get("/question_two")
def get_question_two():
    """
    Question Two: Get average resolution time by company for closed tickets.
    
    Returns:
        List of companies with their average ticket resolution times in seconds
    """
    db_service = DatabaseService()
    try:
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
        results = db_service.execute_query_df(query)
        return {"results": results.to_dict(orient="records")}
    finally:
        db_service.close_connection()


@router.get("/question_three")
def get_question_three():
    """
    Question Three: Get ticket counts by engagement bucket (high/medium/low).
    
    Returns:
        Ticket counts grouped by engagement level buckets
    """
    db_service = DatabaseService()
    try:
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
        results = db_service.execute_query_df(query)
        return {"results": results.to_dict(orient="records")}
    finally:
        db_service.close_connection()


@router.get("/question_three_alternative")
def get_question_three_alternative():
    """
    Question Three: Get ticket counts by engagement bucket (high/medium/low).
    
    Returns:
        Ticket counts grouped by engagement level buckets
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
    db_service = DatabaseService()
    try:
        results = db_service.execute_query_df(query)
        return {"results": results.to_dict(orient="records")}
    finally:
        db_service.close_connection()