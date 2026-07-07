class PromptTemplates:

    @staticmethod
    def function_prompt(source_code: str) -> str:

        return f"""
You are a Senior Python Software Engineer.

Analyze ONLY the following Python function.

Source Code:

{source_code}

Return your answer in Markdown.

Use these headings exactly:

#  Purpose

#  Inputs

#  Output

#  Time Complexity

#  Space Complexity

#  Possible Improvements

#  Example Usage

Do not rewrite the function unless necessary.
Explain in beginner-friendly language.
"""