from src.services.explainer_service import ExplainerService
from src.prompts import PromptTemplates
from src.utils.zip_handler import ZipHandler
import streamlit as st

st.set_page_config(
    page_title="Codebase Explainer AI",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "explanation" not in st.session_state:
    st.session_state.explanation = None

if "function_explanations" not in st.session_state:
    st.session_state.function_explanations = {}

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

input_type = st.radio(
    "Choose Input Type",
    [
        "Python File",
        "ZIP Project"
    ]
)

if input_type == "Python File":

    uploaded_file = st.file_uploader(
        "Choose a Python file",
        type=["py"],
        key="py_upload"
    )

else:

    uploaded_file = st.file_uploader(
        "Choose a ZIP project",
        type=["zip"],
        key="zip_upload"
    )

if input_type == "ZIP Project" and uploaded_file is not None:

    folder = ZipHandler.extract(uploaded_file)

    python_files = ZipHandler.get_python_files(folder)

    service = ExplainerService()

    project = service.parse_multiple_files(python_files,folder)

    st.success("Project parsed successfully!")

    st.write(f"Files: {len(project.files)}")
    st.write(f"Imports: {len(project.imports)}")
    st.write(f"Classes: {len(project.classes)}")
    st.write(f"Functions: {len(project.functions)}")

    st.subheader("Files")

    for file in project.files:
        st.write(f" {file}")

    explanation = service.explain_codebase(project)

    st.divider()

    st.header("AI Codebase Summary")

    st.markdown(explanation)
    

    st.stop()

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if uploaded_file is not None:

    code = uploaded_file.read().decode("utf-8")

    if st.session_state.current_file != uploaded_file.name:

        st.session_state.current_file = uploaded_file.name

        # Clear old cache
        st.session_state.explanation = None
        st.session_state.function_explanations = {}

    try:

        service = ExplainerService()

        project = service.parse_project(code)

        if st.session_state.explanation is None:

            with st.spinner("Analyzing project..."):
                st.session_state.explanation = (
                    service.explain_project(project, code)
                )


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

                st.write("**Source Code:**")

                st.code(
                    func.source_code,
                    language="python"
                )
                if st.button(f"Explain {func.name}",key=f"btn_{func.name}"):

                    if func.cache_key not in st.session_state.function_explanations:

                        with st.spinner(f"Analyzing {func.name}..."):

                            st.session_state.function_explanations[func.cache_key] = (
                                service.explain_function(
                                    func.source_code
                                )
                            )

                    st.markdown(st.session_state.function_explanations[func.cache_key])             

                st.divider()

        else:

            st.write("No functions found.")

    st.divider()

    st.header("AI Explanation")

    st.markdown(st.session_state.explanation)