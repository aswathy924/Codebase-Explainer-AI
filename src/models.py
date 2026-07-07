from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FunctionInfo:
    name: str
    signature: str
    arguments: List[str]
    docstring: Optional[str]
    line: int


@dataclass
class ClassInfo:
    name: str
    line: int
    docstring: Optional[str]
    methods: List[FunctionInfo] = field(default_factory=list)


@dataclass
class ProjectInfo:
    imports: List[str]
    functions: List[FunctionInfo]
    classes: List[ClassInfo]