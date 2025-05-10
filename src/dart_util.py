from pathlib import Path

from src.output_util import OutputType, output


def create_dart_file(path: Path, file_name: str, data: str):
    if path.exists() is False:
        path.mkdir(parents=True, exist_ok=True)

    file_path = path / file_name

    output(f"Creating file: {file_name}", OutputType.INFO)  # noqa: F821
    with open(file_path, "w") as f:
        f.write(data)
