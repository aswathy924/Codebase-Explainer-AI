from src.models import ProjectInfo


class PromptBuilder:

    @staticmethod
    def build_project_prompt(project: ProjectInfo, code: str) -> str:

        imports = "\n".join(
            f"- {imp}" for imp in project.imports
        )

        classes = "\n".join(
            f"- {cls.name}"
            for cls in project.classes
        )

        functions = "\n".join(
            f"- {func.signature}"
            for func in project.functions
        )

        prompt = f"""
You are an expert Python software engineer.

Analyze the following Python project.

## Project Structure

Imports:
{imports if imports else "None"}

Classes:
{classes if classes else "None"}

Functions:
{functions if functions else "None"}

## Source Code

{code}

Please provide:

1. Overall project summary
2. Explain each class
3. Explain each function
4. Mention interesting observations
5. Suggest improvements
6. Explain in beginner-friendly language

Use Markdown formatting.
"""

        return prompt