import sys
from pathlib import Path
from typing import List

from ruamel.yaml import YAML

from src.output_util import OutputType, output


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

    output(f"Created root pubspec.yaml at {pubspec_path}", OutputType.SUCCESS)


def create_root_melos_yaml(path: Path, project_name: str, packages: List[str]) -> None:
    """
    Creates the melos.yaml file for the monorepo workspace with app and package structure.

    Args:
        path: Path where the melos.yaml should be created.
        project_name: The name of the root project.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    melos_data = {
        "name": project_name,
        "packages": ["packages/**", "apps/**"],
        "scripts": {
            "analyze": {"exec": "dart analyze ."},
            "loc": {
                "exec": "flutter gen-l10n",
                "packageFilters": {"fileExists": "l10n.yaml"},
            },
            "svg": {"run": "melos exec --depends-on svg_bin -- dart run svg_bin "},
            "br": {
                "run": "'melos exec --depends-on build_runner -- dart run build_runner build --delete-conflicting-outputs'"
            },
            "release": {
                "exec": "flutter build apk --release",
                "packageFilters": {"ignore": packages},
            },
        },
    }

    melos_path = path / "melos.yaml"
    with melos_path.open("w") as f:
        yaml.dump(melos_data, f)

    output("Created melos.yaml at root", OutputType.SUCCESS)


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
        output(
            f"Skipping {package_name}, pubspec.yaml not found (on workspace resolution)",
            OutputType.ERROR,
        )
        sys.exit()

    try:
        with package_or_app_path.open("r") as f:
            data = yaml.load(f)

        data["resolution"] = "workspace"

        with package_or_app_path.open("w") as f:
            yaml.dump(data, f)

        output(
            f"Added 'resolution: workspace' to {package_or_app_path}",
            OutputType.SUCCESS,
        )

    except Exception as e:
        output(f"Failed to update {package_or_app_path}: {e}", OutputType.ERROR)
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
    output(
        f"Updated workspace in {pubspec_path} with apps and packages.",
        OutputType.SUCCESS,
    )


def create_l10n_yaml(path: Path, is_res: bool, res_package: str) -> bool:
    """
    Creates the l10n yaml file
    return a bool
    """

    if is_res:
        arb_dir = "lib/l10n"
    else:
        arb_dir = f"../../packages/{res_package}/l10n"

    l10n_config = {
        "arb-dir": arb_dir,
        "template-arb-file": "app_en.arb",
        "output-localization-file": "app_localizations.dart",
        "output-class": "AppLocalizations",
        "nullable-getter": False,
        "synthetic-package": False,
    }
    l10n_yaml_path = path / "l10n.yaml"
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    with open(l10n_yaml_path, "w") as f:
        yaml.dump(l10n_config, f)
    output(f"Created l10n.yaml configuration file for {path}", OutputType.SUCCESS)
    return True


def enable_flutter_gen(root_path: Path, res_package: str):
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    pubspec_path = root_path / "pacakges" / res_package

    if not pubspec_path.exists():
        output(f"pubspec didn't exits for {res_package}", OutputType.ERROR)

    with pubspec_path.open("r") as f:
        pubspec_data = yaml.load(f)

    if "flutter" not in pubspec_data:
        output(f"didn't find flutter in pubpspec for {res_package}", OutputType.ERROR)
        return

    if not isinstance(pubspec_data, dict):
        return
    if "generate" not in pubspec_data or not pubspec_data["generate"]:
        pubspec_data["generate"] = True
        output(f"Set generate: true for {res_package}", OutputType.SUCCESS)
    else:
        output(f"generate: true already set for {res_package}", OutputType.SUCCESS)
    with pubspec_path.open("w") as f:
        yaml.dump(
            pubspec_data,
            f,
        )
    output(
        f"Updated workspace in {pubspec_path} with apps and packages.",
        OutputType.SUCCESS,
    )
