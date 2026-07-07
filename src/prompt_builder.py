from src.models import ProjectInfo


class PromptBuilder:

    @staticmethod
    def build_project_prompt(project: ProjectInfo, code: str) -> str:

        imports = "\n".join(
            f"- {imp}" for imp in project.imports
        ) or "None"

        classes = ""

        if project.classes:
            for cls in project.classes:

                methods = "\n".join(
                    f"    - {method.signature}"
                    for method in cls.methods
                ) or "    None"

                classes += f"""
Class: {cls.name}

Methods:
{methods}

Docstring:
{cls.docstring or "None"}

"""

        else:
            classes = "None"

        functions = ""

        if project.functions:

            for func in project.functions:

                functions += f"""
Function: {func.signature}

Docstring:
{func.docstring or "None"}

"""

        else:
            functions = "None"

        prompt = f"""
You are an experienced Senior Python Software Engineer performing a professional code review.

Your audience is a junior developer who has never seen this project before.

Analyze the following Python file.

==========================
PROJECT STRUCTURE
==========================

Imports

{imports}

Classes

{classes}

Functions

{functions}

==========================
SOURCE CODE
==========================

{code}

==========================
TASK
==========================

Write your answer in Markdown.

Use EXACTLY these headings.

# Project Overview

Explain the overall purpose of this file in 3-5 sentences.

# Architecture

Explain how the classes and functions are organized and how they relate.

# Imports

Mention whether imports are necessary or unused.

# Classes

For every class explain:
- Purpose
- Responsibilities
- Important methods

# Functions

For every function explain:
- Purpose
- Inputs
- Output

# Strengths

Mention good software engineering practices used.

# Weaknesses

Mention possible issues, code smells or missing features.

# Suggestions

Suggest realistic improvements.

Rules:

- Do NOT rewrite the code.
- Do NOT explain Python syntax.
- Focus on software design.
- Be concise.
- Be beginner friendly.
- Use Markdown.
"""

        return prompt