from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None