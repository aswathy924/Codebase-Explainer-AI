from src.services.explainer_service import ExplainerService
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

if "codebase_explanation" not in st.session_state:
    st.session_state.codebase_explanation = None

if "file_explanations" not in st.session_state:
    st.session_state.file_explanations = {}

if "project_answers" not in st.session_state:
    st.session_state.project_answers = {}

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

    if st.session_state.get("current_zip") != uploaded_file.name:

        st.session_state.current_zip = uploaded_file.name
        st.session_state.codebase_explanation = None
        st.session_state.file_explanations = {}

    folder = ZipHandler.extract(uploaded_file)

    python_files = ZipHandler.get_python_files(folder)

    service = ExplainerService()

    project = service.parse_multiple_files(
        python_files,
        folder
    )

    st.success("Project parsed successfully!")

    # -------------------------
    # Project Statistics
    # -------------------------

    st.subheader("Project Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Files", len(project.files))
    col2.metric("Imports", len(project.imports))
    col3.metric("Classes", len(project.classes))
    col4.metric("Functions", len(project.functions))

    st.divider()

    # -------------------------
    # Codebase Summary
    # -------------------------

    if st.session_state.codebase_explanation is None:

        with st.spinner("Analyzing entire codebase..."):

            st.session_state.codebase_explanation = (
                service.explain_codebase(project)
            )

    st.header("AI Codebase Summary")

    st.markdown(
        st.session_state.codebase_explanation
    )

    st.divider()

    # -------------------------
    # File Explorer
    # -------------------------

    st.header("File Explorer")

    selected_file = st.selectbox(
        "Choose a file",
        project.files,
        format_func=lambda f: f.path
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "File Details",
            "Source Code",
            "AI Explanation"
        ]
    )

    # -------------------------
    # File Details
    # -------------------------

    with tab1:

        st.subheader("Imports")

        if selected_file.imports:
            for imp in selected_file.imports:
                st.write(f"- {imp}")
        else:
            st.write("No imports")

        st.divider()

        st.subheader("Classes")

        if selected_file.classes:
            for cls in selected_file.classes:
                st.write(f"• {cls.name}")
        else:
            st.write("No classes")

        st.divider()

        st.subheader("Functions")

        if selected_file.functions:
            for func in selected_file.functions:
                st.write(f"• {func.signature}")
        else:
            st.write("No functions")

    # -------------------------
    # Source Code
    # -------------------------

    with tab2:

        st.code(
            selected_file.source_code,
            language="python"
        )

    # -------------------------
    # AI File Explanation
    # -------------------------

    with tab3:

        if selected_file.path not in st.session_state.file_explanations:

            if st.button(
                "Explain This File",
                key=f"explain_{selected_file.path}"
            ):

                with st.spinner("Analyzing file..."):

                    st.session_state.file_explanations[
                        selected_file.path
                    ] = service.explain_file(selected_file)

        if selected_file.path in st.session_state.file_explanations:

            st.markdown(
                st.session_state.file_explanations[
                    selected_file.path
                ]
            )

    st.divider()

    st.header(" AI Project Assistant ")

    question = st.text_area(
        "Ask anything about the uploaded project",
        height=100,
        placeholder="Example: Where is authentication implemented?"
    )

    if st.button("Ask AI"):

        if question.strip():

            if question not in st.session_state.project_answers:

                with st.spinner("Thinking..."):

                    st.session_state.project_answers[question] = (
                        service.answer_question(
                            project,
                            question
                        )
                    )

            st.subheader(" Answer")

            with st.container():
                st.markdown(
                    st.session_state.project_answers[question]
                )

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

    with col1:

        st.subheader("Code Preview")

        st.code(code, language="python")

    with col2:

        st.subheader("File Details")

        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size} bytes")
        st.write(f"**Lines:** {len(code.splitlines())}")

        st.divider()

        st.subheader("Imports")

        if project.imports:

            for imp in project.imports:
                st.write(f" {imp}")

        else:

            st.write("No imports found.")

        st.divider()

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