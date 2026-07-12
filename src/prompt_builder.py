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

        files = ""

        if project.files:
            files = "\n".join(
                f"- {file}"
                for file in project.files
            )

        else:
            files = "Current analysis contains a single Python file."

        prompt = f"""
You are an experienced Senior Python Software Engineer performing a professional code review.

Your audience is a junior developer who has never seen this project before.

Analyze the following Python codebase. It may contain one or more Python files.

==========================
PROJECT STRUCTURE
==========================

Imports

{imports}

Classes

{classes}

Functions

{functions}

Files

{files}

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


    @staticmethod
    def build_codebase_prompt(summary: str):

        return f"""
    You are a Senior Software Architect.

    Below is a structural summary of an entire Python project.

    {summary}

    Your task is to explain the project.

    Return Markdown.

    # Project Purpose

    Explain what the project most likely does.

    # Architecture

    Explain how the project is organized.

    # Folder Organization

    Explain the purpose of each folder.

    # Important Components

    Mention important modules and their responsibilities.

    # Strengths

    Mention good design choices.

    # Suggestions

    Suggest realistic improvements.

    Be concise.
    """

    @staticmethod
    def build_function_prompt(source_code):

        return f"""
    You are an experienced Python software engineer.

    Explain this function.

    ==========================
    FUNCTION
    ==========================

    {source_code}

    ==========================
    TASK
    ==========================

    Use EXACTLY these headings.

    # Purpose

    What does this function do?

    # Parameters

    Explain each parameter.

    # Return Value

    Explain what is returned.

    # How It Works

    Explain the logic step by step.

    # Possible Improvements

    Mention realistic improvements.

    Rules:

    - Be beginner friendly.
    - Do not rewrite the code.
    - Do not explain Python syntax.
    """

    @staticmethod
    def build_file_prompt(file) -> str:

        imports = "\n".join(
            f"- {imp}" for imp in file.imports
        ) or "None"

        classes = ""

        if file.classes:

            for cls in file.classes:

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

        if file.functions:

            for func in file.functions:

                functions += f"""
    Function: {func.signature}

    Docstring:
    {func.docstring or "None"}

    """

        else:
            functions = "None"

        return f"""
    You are an experienced Senior Python Software Engineer.

    Analyze ONE Python source file from a larger software project.

    Do NOT describe the entire project.
    Focus only on this file.

    ==========================
    FILE
    ==========================

    Path:
    {file.path}

    ==========================
    IMPORTS
    ==========================

    {imports}

    ==========================
    CLASSES
    ==========================

    {classes}

    ==========================
    FUNCTIONS
    ==========================

    {functions}

    ==========================
    SOURCE CODE
    ==========================

    {file.source_code}

    ==========================
    TASK
    ==========================

    Write your answer in Markdown.

    Use EXACTLY these headings.

    # File Purpose

    Explain the responsibility of this file.

    # Main Components

    Explain the important classes and functions.

    # Dependencies

    Explain why the imported modules are needed.

    # How This File Fits Into The Project

    Explain how this file interacts with the rest of the project.

    # Strengths

    Mention good software engineering practices.

    # Weaknesses

    Mention possible issues or missing features.

    # Suggestions

    Suggest realistic improvements.

    Rules:

    - Do NOT explain Python syntax.
    - Do NOT rewrite the code.
    - Do NOT invent functionality.
    - If information is unavailable, say so.
    - Be concise.
    """