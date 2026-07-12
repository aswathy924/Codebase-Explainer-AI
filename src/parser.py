import ast
from typing import List

from src.models import FunctionInfo, ClassInfo, ProjectInfo


class CodeParser:

    def __init__(self, code: str):

        self.code = code

        try:
            self.tree = ast.parse(code)

        except SyntaxError as e:
            raise ValueError(f"Invalid Python code:\n{e}")

    # -------------------------
    # Helper Methods
    # -------------------------

    def _get_arguments(self, node) -> List[str]:
        return [arg.arg for arg in node.args.args]

    def _get_docstring(self, node):
        return ast.get_docstring(node)

    def _format_signature(self, node):

        args = self._get_arguments(node)

        return f"{node.name}({', '.join(args)})"

    # -------------------------
    # Imports
    # -------------------------

    def get_imports(self):

        imports = []

        for node in self.tree.body:

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                imports.append(node.module)

        return imports

    # -------------------------
    # Functions
    # -------------------------

    def get_functions(self):

        functions = []

        for node in self.tree.body:

            if isinstance(node, ast.FunctionDef):

                functions.append(

                    FunctionInfo(

                        name=node.name,
                        signature=self._format_signature(node),
                        arguments=self._get_arguments(node),
                        docstring=self._get_docstring(node),
                        line=node.lineno,
                        source_code=ast.get_source_segment(
                            self.code,
                            node
                        )
                    )
                )

        return functions

    # -------------------------
    # Classes
    # -------------------------

    def get_classes(self):

        classes = []

        for node in self.tree.body:

            if isinstance(node, ast.ClassDef):

                methods = []

                for item in node.body:

                    if isinstance(item, ast.FunctionDef):

                        methods.append(

                            FunctionInfo(
                                name=item.name,
                                signature=self._format_signature(item),
                                arguments=self._get_arguments(item),
                                docstring=self._get_docstring(item),
                                line=item.lineno,
                                source_code=ast.get_source_segment(
                                    self.code,
                                    item
                                )
                            )
                        )

                classes.append(

                    ClassInfo(
                        name=node.name,
                        line=node.lineno,
                        docstring=self._get_docstring(node),
                        methods=methods
                    )
                )

        return classes

    # -------------------------
    # Project Analysis
    # -------------------------

    def analyze(self):

        return ProjectInfo(
            imports=self.get_imports(),
            functions=self.get_functions(),
            classes=self.get_classes(),
            files = []
        )