# 🤖 Codebase Explainer AI

An AI-powered code analysis platform that helps developers quickly understand unfamiliar Python projects. The application parses Python source code using Abstract Syntax Trees (AST), extracts structural information, and leverages Large Language Models (LLMs) to generate intelligent explanations at the project, file, and function levels.

In addition to automated code explanations, the application supports multi-file project analysis, interactive project exploration, and natural language question answering over uploaded Python codebases.

---

## 🚀 Features

### 📄 Single File Analysis
- Upload any Python (`.py`) file
- Detect imports, classes, methods, and functions
- Display source code with extracted metadata
- Generate AI-powered project explanations
- Generate function-level explanations

---

### 📦 Complete Codebase Analysis
- Upload an entire Python project as a ZIP archive
- Automatically extract and parse every Python file
- Merge project metadata into a single codebase representation
- Generate a high-level AI summary of the entire project

---

### 📁 File Explorer
Browse every Python file inside the uploaded project.

For each file:
- View imports
- View classes
- View functions
- Read the complete source code
- Generate file-specific AI explanations

---

### 💬 AI Project Assistant
Ask questions about the uploaded project in natural language.

Example questions:

- Where is authentication implemented?
- Explain the folder structure.
- Which file handles products?
- Where should I add a new API endpoint?
- Which files contain business logic?

The assistant answers using the parsed project structure and metadata.

---

## 🏗 Architecture

```
                Upload File / ZIP
                       │
                       ▼
                Code Parser (AST)
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Project Metadata              File Metadata
        │                             │
        └──────────────┬──────────────┘
                       ▼
               Prompt Builder
                       │
                       ▼
                  Gemini LLM
                       │
                       ▼
          AI Generated Explanations
```

---

## ⚙ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI
- Google Gemini API

### Parsing
- Python AST (Abstract Syntax Tree)

### Other Libraries
- pathlib
- tempfile
- zipfile
- dataclasses
- hashlib

---

## ▶ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Codebase-Explainer-AI.git
```

Move into the project directory

```bash
cd Codebase-Explainer-AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```


