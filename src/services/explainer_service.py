from src.parser import CodeParser
from src.prompt_builder import PromptBuilder
from src.prompts import PromptTemplates
from src.llm import LLMClient
from src.models import ProjectInfo


class ExplainerService:

    def __init__(self):
        self.llm = LLMClient()

    # -------------------------
    # Parse Project
    # -------------------------

    def parse_project(self, code: str) -> ProjectInfo:

        parser = CodeParser(code)

        return parser.analyze()

    # -------------------------
    # Explain Project
    # -------------------------

    def explain_project(
        self,
        project: ProjectInfo,
        code: str
    ) -> str:

        prompt = PromptBuilder.build_project_prompt(
            project,
            code
        )

        return self.llm.generate(prompt)

    # -------------------------
    # Explain Function
    # -------------------------

    def explain_function(
        self,
        source_code: str
    ) -> str:

        prompt = PromptTemplates.function_prompt(
            source_code
        )

        return self.llm.generate(prompt)