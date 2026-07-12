from src.models import ProjectInfo


class CodebaseSummary:

    @staticmethod
    def build(project: ProjectInfo):

        summary = []

        summary.append("PROJECT SUMMARY")
        summary.append("=" * 40)

        summary.append(f"Files: {len(project.files)}")
        summary.append(f"Imports: {len(project.imports)}")
        summary.append(f"Classes: {len(project.classes)}")
        summary.append(f"Functions: {len(project.functions)}")

        summary.append("\nFILES")

        for file in project.files:
            summary.append(f"- {file}")

        summary.append("\nIMPORTS")

        for imp in sorted(project.imports):
            summary.append(f"- {imp}")

        summary.append("\nCLASSES")

        for cls in project.classes:
            summary.append(f"- {cls.name}")

        summary.append("\nFUNCTIONS")

        for func in project.functions:
            summary.append(f"- {func.signature}")

        return "\n".join(summary)