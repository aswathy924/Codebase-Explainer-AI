from src.parser import CodeParser
from src.prompt_builder import PromptBuilder
from src.prompts import PromptTemplates
from src.llm import LLMClient
from src.models import ProjectInfo
from src.services.codebase_summary import CodebaseSummary


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


    def merge_projects(self, projects):

        merged = ProjectInfo()

        for project in projects:

            merged.imports.extend(project.imports)
            merged.functions.extend(project.functions)
            merged.classes.extend(project.classes)
            merged.files.extend(project.files)

        merged.imports = sorted(set(merged.imports))

        return merged

    def parse_multiple_files(self, python_files, root_folder):

        projects = []

        for file in python_files:

            code = file.read_text(encoding="utf-8")

            parser = CodeParser(code)

            project = parser.analyze()

            project.files.append(
                file.relative_to(root_folder).as_posix()
            )

            projects.append(project)

        return self.merge_projects(projects)

    def explain_codebase(self, project):

        summary = CodebaseSummary.build(project)

        prompt = PromptBuilder.build_codebase_prompt(
            summary
        )

        return self.llm.generate(prompt)