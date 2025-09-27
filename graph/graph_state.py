from typing import TypedDict

class GraphState(TypedDict):
    question: str
    file_name: str | None
    answer: str | None
    token_input: int | None
    token_output: int | None