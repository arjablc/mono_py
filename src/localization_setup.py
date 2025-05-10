import json
import subprocess
from pathlib import Path
from typing import List

from src.constants import L10N, LIB, SRC
from src.dart_util import create_dart_file
from src.output_util import OutputType, output
from src.package_util import add_package
from src.templates import apps_main_template, get_res_l10n_template
from src.yaml import create_l10n_yaml

# def find_res_package(root_path: Path, packages: List[str]) -> Path:

en_arb_content = {
    "@@locale": "en",
    "appTitle": "monorepo",
    "@appTitle": {"description": "The title of the application"},
    "helloWorld": "Hello World!",
    "@helloWorld": {"description": "A traditional greeting"},
    "greeting": "Hello {username}",
    "@greeting": {
        "description": "A greeting with a parameter",
        "placeholders": {"username": {"type": "String", "example": "John"}},
    },
    "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
    "@itemCount": {
        "description": "A plural message example",
        "placeholders": {"count": {"type": "num", "format": "compact"}},
    },
}

ne_arb_content = {
    "@@locale": "ne",
    "appTitle": "मोनोरेपो",
    "@appTitle": {"description": "The title of the application"},
    "helloWorld": "नमस्कार संसार!",
    "@helloWorld": {"description": "A traditional greeting"},
    "greeting": "नमस्कार {username}",
    "@greeting": {
        "description": "A greeting with a parameter",
        "placeholders": {"username": {"type": "String", "example": "John"}},
    },
    "itemCount": "{count, plural, =0{कुनै वस्तु छैन} =1{१ वस्तु} other{{count} वस्तुहरू}}",
    "@itemCount": {
        "description": "A plural message example",
        "placeholders": {"count": {"type": "num", "format": "compact"}},
    },
}


def setup_localization(
    project_name: str, package_name: str, root_path: Path, apps: List[str]
):
    output("Starting localization setup...", OutputType.INFO)

    package_pubspec = root_path / "packages" / package_name / "pubspec.yaml"
    package_path = root_path / "packages" / package_name

    output(f"Checking resource package at: {package_path}", OutputType.INFO)
    if package_path.exists() is False:
        output("Resource package path doesn't exist", OutputType.ERROR)
        return

    output(f"Checking package pubspec at: {package_pubspec}", OutputType.INFO)
    if package_pubspec.exists() is False:
        output("Resource package pubspec doesn't exist", OutputType.ERROR)
        return

    # install flutter localization
    output("Adding flutter_localizations package...", OutputType.INFO)
    try:
        subprocess.run(
            ["flutter", "pub", "add", "flutter_localizations", "--sdk=flutter"],
            check=True,
            cwd=package_path,
            capture_output=True,
        )
        output("Added flutter_localizations package", OutputType.SUCCESS)
    except subprocess.CalledProcessError:
        output("Failed to add flutter_localizations package", OutputType.ERROR)
        return

    # Install intl package
    output("Adding intl package...", OutputType.INFO)
    add_package(pub_path=package_path, package_name="intl", is_dev=False)
    output("Added intl package", OutputType.SUCCESS)

    # create arb files
    arb_folder = package_path / LIB / L10N
    output(f"Setting up localization files in: {arb_folder}", OutputType.INFO)
    if arb_folder.exists():
        output("Localization folder already exists", OutputType.INFO)
        return
    arb_folder.mkdir(parents=True, exist_ok=True)
    arb_file_en = arb_folder / "app_en.arb"
    arb_file_np = arb_folder / "app_ne.arb"

    output("Creating English localization file...", OutputType.INFO)
    with arb_file_en.open("w") as f:
        json.dump(en_arb_content, f, ensure_ascii=False, indent=2)

    output("Creating Nepali localization file...", OutputType.INFO)
    with arb_file_np.open("w") as f:
        json.dump(ne_arb_content, f, ensure_ascii=False, indent=2)

    output("Created the ARB files", OutputType.SUCCESS)

    # Creating the l10n yaml file for package
    output("Creating l10n.yaml for resource package...", OutputType.INFO)
    create_l10n_yaml(path=package_path, is_res=True, res_package=package_name)

    # Creating l10n yaml for apps
    output("Setting up localization for apps...", OutputType.INFO)
    for app in apps:
        output(f"Configuring localization for app: {app}", OutputType.INFO)
        app_path = root_path / "apps" / app
        app_lib_path = app_path / LIB
        if app_lib_path.exists() is False:
            output(f"Creating lib directory for app: {app}", OutputType.INFO)
            app_lib_path.mkdir(parents=True, exist_ok=True)
        app_dart_path = app_path / LIB / "app"
        main_file_name = f"{app}_app.dart"
        create_l10n_yaml(path=app_path, is_res=False, res_package=package_name)
        create_dart_file(
            app_dart_path, main_file_name, apps_main_template(app, project_name)
        )

    output("Creating localization source files...", OutputType.INFO)
    src_path = package_path / LIB / SRC

    if src_path.exists() is False:
        output("Creating src directory...", OutputType.INFO)
        src_path.mkdir(parents=True, exist_ok=True)

    localization_path = src_path / f"{project_name}_localization.dart"
    output(f"Creating localization class file: {localization_path}", OutputType.INFO)
    with open(localization_path, "w") as f:
        f.write(get_res_l10n_template(f"{project_name}"))
    output("Localization setup completed successfully!", OutputType.SUCCESS)
