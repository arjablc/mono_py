from pathlib import Path

from src.constants import LIB, SRC
from src.dart_util import create_dart_file
from src.output_util import OutputType, output
from src.package_util import add_package
from src.templates import get_theme_template


def setup_themes(
    project_name: str,
    package_name: str,
    root_path: Path,
):

    package_path = root_path / "packages" / package_name
    src_path = package_path / LIB / SRC
    theme_file_name = f"{project_name}_theme.dart"

    output("Installing google_fonts for resources", OutputType.INFO)
    add_package(package_path, "google_fonts", is_dev=False)

    output(f"Creating theme  class file: {theme_file_name}", OutputType.INFO)
    create_dart_file(src_path, theme_file_name, get_theme_template(project_name))
    output("Theme setup completed successfully!", OutputType.SUCCESS)
