import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from yaml_util import add_resolution_workspace_to_packages


def add_package(
    pub_path: Path,
    package_name: str,
    is_dev: bool,
) -> None:
    """
    Adds a Dart/Flutter package using `flutter pub add` or `flutter pub add --dev`.

    Args:
        pubspec_dir: The directory where the pubspec.yaml is located.
        package_name: The name of the package to add. dev: If True, add as a dev dependency.
    Returns:
        True if the command succeeded, False otherwise.
    """

    cmd = ["flutter", "pub", "add"]
    if is_dev:
        cmd.append("-d")
    cmd.append(package_name)

    try:
        subprocess.run(cmd, cwd=pub_path, check=True)
        print(f"added {package_name} as {'as dev' if is_dev else ''}")
    except subprocess.CalledProcessError:
        print(f" Failed to add package '{package_name}' in {pub_path}")
        sys.exit()


def create_flutter_templates(monorepo_path: Path, apps: list, is_app: bool):
    """
    creates the basic flutter application
    for  all the application names that are provided
    """
    if is_app:
        app_path = monorepo_path / "apps"
    else:
        app_path = monorepo_path / "packages"
    app_path.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        if is_app:
            list(
                executor.map(
                    lambda app: single_flutter_app_template(app_path, app), apps
                )
            )
        else:
            list(
                executor.map(
                    lambda app: single_flutter_package_template(app_path, app), apps
                )
            )


def single_flutter_app_template(app_path: Path, app: str) -> bool:
    """
    Does the thing for single app
    """
    cmd = ["flutter", "create", app]
    try:
        print(f"creating for {app}")
        subprocess.run(cmd, cwd=app_path, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(f"failed to create app for {app}")
        return False

    app_pubspec_path = app_path / app / "pubspec.yaml"
    add_resolution_workspace_to_packages(app_pubspec_path, app)
    print(f"created for {app}")
    return True


def single_flutter_package_template(package_path: Path, package: str) -> bool:
    """
    Does the thing for single package
    """
    cmd = ["flutter", "create", "-t", "package", package]
    try:
        print(f"creating for {package}")
        subprocess.run(cmd, cwd=package_path, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(f"failed to create package for {package}")
        return False

    package_pubspec_path = package_path / package / "pubspec.yaml"
    add_resolution_workspace_to_packages(package_pubspec_path, package)
    print(f"created for {package}")
    return True
