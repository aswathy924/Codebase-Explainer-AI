from src.parser import CodeParser
from src.prompt_builder import PromptBuilder
from src.llm import LLMClient
import streamlit as st

st.set_page_config(
    page_title="Codebase Explainer AI",
    layout="wide"
)

st.title("Codebase Explainer AI")

st.write(
    "Upload a Python file and I'll analyze its structure."
)

# Sidebar
with st.sidebar:

    st.header("About")

    st.write("""
    This application analyzes Python source code.

    Features:
    - Upload Python files
    - Detect imports
    - Detect classes
    - Detect methods
    - Detect functions
    - Display metadata
    """)

uploaded_file = st.file_uploader(
    "Choose a Python file",
    type=["py"]
)

if uploaded_file is not None:

    code = uploaded_file.read().decode("utf-8")

    try:

        parser = CodeParser(code)

        project = parser.analyze()

        prompt = PromptBuilder.build_project_prompt(
            project,
            code
        )

        llm = LLMClient()

        with st.spinner("Analyzing your code..."):

            explanation = llm.generate(prompt)

    except ValueError as e:

        st.error(str(e))
        st.stop()

    st.success("File uploaded successfully!")

    col1, col2 = st.columns([3, 1])

    # -------------------------
    # LEFT COLUMN
    # -------------------------

    with col1:

        st.subheader("Code Preview")

        st.code(code, language="python")

    # -------------------------
    # RIGHT COLUMN
    # -------------------------

    with col2:

        st.subheader("File Details")

        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size} bytes")
        st.write(f"**Lines:** {len(code.splitlines())}")

        st.divider()

        # -------------------------
        # IMPORTS
        # -------------------------

        st.subheader("Imports")

        if project.imports:

            for imp in project.imports:
                st.write(f" {imp}")

        else:

            st.write("No imports found.")

        st.divider()

        # -------------------------
        # CLASSES
        # -------------------------

        st.subheader("Classes")

        if project.classes:

            for cls in project.classes:

                st.markdown(f"### {cls.name}")

                st.write(f"**Line:** {cls.line}")

                st.write(f"**Docstring:** {cls.docstring or 'No docstring'}")

                if cls.methods:

                    st.write("**Methods:**")

                    for method in cls.methods:

                        st.write(
                            f"• {method.signature} (Line {method.line})"
                        )

                st.divider()

        else:

            st.write("No classes found.")

        # -------------------------
        # FUNCTIONS
        # -------------------------

        st.subheader("Functions")

        if project.functions:

            for func in project.functions:

                st.markdown(f"### {func.name}")

                st.write(f"**Signature:** {func.signature}")

                st.write(
                    f"**Arguments:** {', '.join(func.arguments) if func.arguments else 'None'}"
                )

                st.write(f"**Line:** {func.line}")

                st.write(
                    f"**Docstring:** {func.docstring or 'No docstring'}"
                )

                st.divider()

        else:

            st.write("No functions found.")

    st.divider()

    st.header("AI Explanation")

    st.markdown(explanation)