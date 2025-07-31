from fastapi import APIRouter
from models.input_models import QuestionOneInput, QuestionTwoInput
from services.string_services import (
    normalize_strings_manual,
    normalize_strings_built_in,
)
from services.dictionary_services import (
    flatten_dictionary_iterative,
    flatten_dictionary_recursive,
    flatten_dictionary_library,
)

router = APIRouter(prefix="/python")


# =============================================================================
# QUESTION ONE ENDPOINTS - String Normalization
# =============================================================================


@router.post("/question_one_manual")
def get_question_one_manual(input: QuestionOneInput) -> dict:
    """
    Manually normalize strings without using built-in methods.
    Converts to lowercase and removes leading/trailing whitespace.

    Args:
        input: QuestionOneInput containing list of strings to normalize

    Returns:
        Dictionary with normalized strings as keys and their frequencies as values
    """
    return normalize_strings_manual(input.Type)


@router.post("/question_one_built_in")
def get_question_one_built_in(input: QuestionOneInput) -> dict:
    """
    Use the built-in lower and strip methods to normalize strings.

    Args:
        input: QuestionOneInput containing list of strings to normalize

    Returns:
        Dictionary with normalized strings as keys and their frequencies as values
    """
    return normalize_strings_built_in(input.Type)


# =============================================================================
# QUESTION TWO ENDPOINTS - Dictionary Flattening
# =============================================================================


@router.post("/question_two_iterative")
def get_question_two_iterative(input: QuestionTwoInput) -> dict:
    """
    Flatten a nested dictionary using iterative approach with stack.

    Args:
        input: QuestionTwoInput containing dictionary and delimiter

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    return flatten_dictionary_iterative(input.dictionary, input.delimiter)


@router.post("/question_two_recursive")
def get_question_two_recursive(input: QuestionTwoInput) -> dict:
    """
    Flatten a nested dictionary using recursive approach.

    Args:
        input: QuestionTwoInput containing dictionary, parent key, and delimiter

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    return flatten_dictionary_recursive(
        input.dictionary, input.parent_key, input.delimiter
    )


@router.post("/question_two_library")
def get_question_two_library(input: QuestionTwoInput) -> dict:
    """
    Flatten a nested dictionary using the flatdict library.

    Args:
        input: QuestionTwoInput containing dictionary and delimiter

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    return flatten_dictionary_library(input.dictionary, input.delimiter)
