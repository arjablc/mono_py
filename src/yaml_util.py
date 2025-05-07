import sys
from pathlib import Path
from typing import List

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


def add_resolution_workspace_to_packages(
    package_or_app_path: Path, package_name: str
) -> None:
    """
    Adds 'resolution: workspace' to the pubspec.yaml of each package in the packages directory.

    Args:
        packages_dir: Path to the 'packages' directory.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    if not package_or_app_path.exists():
        print(
            f"Skipping {package_name}, pubspec.yaml not found.(on workspace resolution)"
        )
        sys.exit()

    try:
        with package_or_app_path.open("r") as f:
            data = yaml.load(f)

        data["resolution"] = "workspace"

        with package_or_app_path.open("w") as f:
            yaml.dump(data, f)

        print(f"Added 'resolution: workspace' to {package_or_app_path}")

    except Exception as e:
        print(f" Failed to update {package_or_app_path}: {e}")
        sys.exit()


def add_to_workspace(monorepo_path: Path, apps: List[str], packages: List[str]):
    """
    Adds the provided apps and packages to the workspace section of the root pubspec.yaml.

    Args:
        monorepo_path: Path to the root
        apps: List of app names to be added to the workspace.
        packages: List of package names to be added to the workspace.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    pubspec_path = monorepo_path / "pubspec.yaml"

    with pubspec_path.open("r") as f:
        pubspec_data = yaml.load(f)
    if "workspace" not in pubspec_data:
        pubspec_data["workspace"] = []
    workspace_entries = pubspec_data["workspace"]
    for package in packages:
        package_path = f"packages/{package}"
        if package_path not in workspace_entries:
            workspace_entries.append(package_path)
    for app in apps:
        app_path = f"apps/{app}"
        if app_path not in workspace_entries:
            workspace_entries.append(app_path)
    with pubspec_path.open("w") as f:
        yaml.dump(
            pubspec_data,
            f,
        )
    print(f"Updated workspace in {pubspec_path} with apps and packages.")


def create_l10n_yaml(path: Path, is_res: bool, res_package: str) -> bool:
    """
    Creates the l10n yaml file
    return a bool
    """

    if is_res:
        arb_dir = "lib/l10n"
    else:
        arb_dir = f"../{res_package}/l10n"

    l10n_config = {
        "arb-dir": arb_dir,
        "template-arb-file": "app_en.arb",
        "output-localization-file": "app_localizations.dart",
        "output-class": "AppLocalizations",
        "nullable-getter": "false",
    }
    l10n_yaml_path = path / "l10n.yaml"
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    with open(l10n_yaml_path, "w") as f:
        yaml.dump(l10n_config, f)
    print("✓ Created l10n.yaml configuration file")
    return True
