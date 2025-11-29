from dataclasses import dataclass
from typing import Any


@dataclass
class CodeOutputModel:
    output: Any
    logs: str
    is_final_answer: bool
