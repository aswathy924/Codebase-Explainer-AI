import zipfile
import tempfile
from pathlib import Path


class ZipHandler:

    @staticmethod
    def extract(zip_file):

        temp_dir = tempfile.mkdtemp()

        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        return Path(temp_dir)

    @staticmethod
    def get_python_files(folder):

        return list(folder.rglob("*.py"))