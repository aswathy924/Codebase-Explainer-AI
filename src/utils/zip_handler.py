import io
import zipfile
import tempfile
from pathlib import Path


class ZipHandler:

    @staticmethod
    def extract(zip_file):

        temp_dir = tempfile.mkdtemp()

        zip_bytes = zip_file.getvalue()

        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        return Path(temp_dir)

    @staticmethod
    def get_python_files(folder):

        return list(folder.rglob("*.py"))