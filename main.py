import argparse
import sys
from pathlib import Path

from src.constants import LIB
from src.dart_util import create_dart_file
from src.input_util import take_user_input
from src.localization_setup import setup_localization
from src.melos_util import is_melos_installed, melos_command
from src.output_util import OutputType, output
from src.package_util import add_package, create_flutter_templates, pub_get
from src.templates import res_export_template
from src.theme_setup import setup_themes
from src.yaml import (add_to_workspace, create_root_melos_yaml,
                      create_root_pubspec_yaml)


def is_flutter_monorepo(path: Path) -> bool:
    """
    Check if the given path is a Flutter Melos monorepo by verifying essential files.

    Args:
        path: Path to check

    Returns:
        bool: True if it's a valid Flutter Melos monorepo, False otherwise
    """
    required_files = ["melos.yaml", "pubspec.yaml"]
    return all((path / file).exists() for file in required_files)


def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Flutter Monorepo Setup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new monorepo
  python main.py

  # Add to existing monorepo
  python main.py --add /path/to/monorepo
        """,
    )

    parser.add_argument(
        "--add",
        type=str,
        help="Path to existing Flutter Melos monorepo to add new packages/apps",
        metavar="PATH",
    )

    return parser.parse_args()


def main():
    """
    Entry point
    """
    args = parse_args()

    if args.add:
        monorepo_path = Path(args.add)
        if not monorepo_path.exists():
            output(f"Path '{args.add}' does not exist.", OutputType.ERROR)
            sys.exit(1)

        if not monorepo_path.is_dir():
            output(f"Path '{args.add}' is not a directory.", OutputType.ERROR)
            sys.exit(1)

        if not is_flutter_monorepo(monorepo_path):
            output(
                f"Path '{args.add}' is not a valid Flutter Melos monorepo. "
                "Required files (melos.yaml, pubspec.yaml) not found.",
                OutputType.ERROR,
            )
            sys.exit(1)

        if not is_melos_installed():
            output(
                "Melos is not installed. Please install Melos first:\n"
                "dart pub global activate melos",
                OutputType.ERROR,
            )
            sys.exit(1)

        output(f"Adding to existing monorepo at: {monorepo_path}", OutputType.INFO)
        input = take_user_input()
        create_flutter_templates(monorepo_path, input.apps, is_app=True)
        create_flutter_templates(monorepo_path, input.packages, is_app=False)
        add_to_workspace(monorepo_path, input.apps, input.packages)
        return

    # Create new monorepo
    output("Flutter monorepo setup:", OutputType.INFO)
    input = take_user_input()
    project_name = input.project_name
    if project_name is None:
        return
    monorepo_path = Path.cwd() / project_name
    try:
        monorepo_path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        output(f"Folder '{project_name}' already exists.", OutputType.ERROR)
        sys.exit(1)

    output(f"Created folder: {monorepo_path}", OutputType.SUCCESS)
    create_root_pubspec_yaml(monorepo_path, project_name)
    add_package(monorepo_path, "melos", True)
    create_root_melos_yaml(monorepo_path, project_name, input.packages)
    create_flutter_templates(monorepo_path, input.apps, is_app=True)
    create_flutter_templates(monorepo_path, input.packages, is_app=False)
    add_to_workspace(monorepo_path, input.apps, input.packages)
    res_package = project_name + "_resources"
    setup_localization(project_name, res_package, monorepo_path, input.apps)
    setup_themes(
        project_name,
        res_package,
        monorepo_path,
    )
    melos_command(monorepo_path, ["bs"])
    melos_command(monorepo_path, ["loc"])
    project_path = monorepo_path / "packages" / res_package / LIB
    file_name = f"{res_package}.dart"
    create_dart_file(project_path, file_name, res_export_template(project_name))
    pub_get(monorepo_path)


if __name__ == "__main__":
    main()
