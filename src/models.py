from dataclasses import dataclass, field
from typing import List, Optional
import hashlib


@dataclass
class FunctionInfo:
    name: str
    signature: str
    arguments: List[str]
    docstring: Optional[str]
    line: int
    source_code: str

    @property
    def cache_key(self) -> str:
        return hashlib.sha256(
            self.source_code.encode()
        ).hexdigest()


@dataclass
class ClassInfo:
    name: str
    line: int
    docstring: Optional[str]
    methods: List[FunctionInfo] = field(default_factory=list)


@dataclass
class ProjectInfo:
    imports: List[str] = field(default_factory=list)
    functions: List[FunctionInfo] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)

    files: List[str] = field(default_factory=list)