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


@router.post("/question_one_manual")
def get_question_one_manual(input: QuestionOneInput) -> dict:
    return normalize_strings_manual(input.Type)


@router.post("/question_one_built_in")
def get_question_one_built_in(input: QuestionOneInput) -> dict:
    return normalize_strings_built_in(input.Type)


@router.post("/question_two_iterative")
def get_question_two_iterative(input: QuestionTwoInput) -> dict:
    return flatten_dictionary_iterative(input.dictionary, input.delimiter)


@router.post("/question_two_recursive")
def get_question_two_recursive(input: QuestionTwoInput) -> dict:
    return flatten_dictionary_recursive(
        input.dictionary, input.parent_key, input.delimiter
    )


@router.post("/question_two_library")
def get_question_two_library(input: QuestionTwoInput) -> dict:
    return flatten_dictionary_library(input.dictionary, input.delimiter)
