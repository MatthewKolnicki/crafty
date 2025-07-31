from fastapi import APIRouter
from services.sql_query_services import SQLQueryService

router = APIRouter(prefix="/sql")


@router.get("/question_one")
def get_question_one():
    """
    Question One: Get engagement counts by company for the last 30 days.

    Returns:
        List of companies with their engagement counts for the last 30 days
    """
    sql_service = SQLQueryService()
    return sql_service.get_engagement_counts_by_company()


@router.get("/question_two")
def get_question_two():
    """
    Question Two: Get average resolution time by company for closed tickets.

    Returns:
        List of companies with their average ticket resolution times in seconds
    """
    sql_service = SQLQueryService()
    return sql_service.get_average_resolution_time_by_company()


@router.get("/question_three")
def get_question_three():
    """
    Question Three: Get ticket counts by engagement bucket (high/medium/low).

    Returns:
        Ticket counts grouped by engagement level buckets
    """
    sql_service = SQLQueryService()
    return sql_service.get_ticket_counts_by_engagement_bucket()


@router.get("/question_three_alternative")
def get_question_three_alternative():
    """
    Question Three: Get ticket counts by engagement bucket (high/medium/low).

    Returns:
        Ticket counts grouped by engagement level buckets
    """
    sql_service = SQLQueryService()
    return sql_service.get_ticket_counts_by_engagement_bucket_alternative()
