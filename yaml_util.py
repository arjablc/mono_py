import sys
from pathlib import Path

from ruamel.yaml import YAML


def create_root_pubspec_yaml(path: Path, project_name: str) -> None:
    """
    Creates a pubspec.yaml at the root of the monorepo.

    Args:
        path: Path where the pubspec.yaml should be created.
        project_name: The name of the root project.
    """

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    pubspec_data = {
        "name": project_name,
        "publish_to": "none",
        "environment": {"sdk": ">=3.6.0 <4.0.0"},
        "workspace": [],
    }

    pubspec_path = path / "pubspec.yaml"
    with pubspec_path.open("w") as f:
        yaml.dump(pubspec_data, f)

    print(f"📄 Created root pubspec.yaml at {pubspec_path}")


def create_root_molos_yaml(path: Path, project_name: str) -> None:
    """
    Creates the melos.yaml file for the monorepo workspace with app and package structure.

    Args:
        path: Path where the melos.yaml should be created.
        project_name: The name of the root project.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    melos_data = {"name": project_name, "packages": ["packages/**", "apps/**"]}

    melos_path = path / "melos.yaml"
    with melos_path.open("w") as f:
        yaml.dump(melos_data, f)

    print("Created melos.yaml at root")


def add_resolution_workspace_to_packages(pubspec_path: Path, package_name: str) -> None:
    """
    Adds 'resolution: workspace' to the pubspec.yaml of each package in the packages directory.

    Args:
        packages_dir: Path to the 'packages' directory.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    if not pubspec_path.exists():
        print(f"⚠️ Skipping {package_name}, pubspec.yaml not found.")
        sys.exit()

    try:
        with pubspec_path.open("r") as f:
            data = yaml.load(f)

        data["resolution"] = "workspace"

        with pubspec_path.open("w") as f:
            yaml.dump(data, f)

        print(f"Added 'resolution: workspace' to {pubspec_path}")

    except Exception as e:
        print(f" Failed to update {pubspec_path}: {e}")
        sys.exit()
