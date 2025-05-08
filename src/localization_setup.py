import json
import subprocess
from pathlib import Path
from typing import List

from src.package_util import add_package
from src.yaml import create_l10n_yaml
from src.output_util import output, OutputType

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

np_arb_content = {
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


def setup_localization(package_name: str, root_path: Path, apps: List[str]):

    package_pubspec = root_path / "packages"/ package_name / "pubspec.yaml"
    package_path = root_path / "packages" / package_name

    if package_path.exists() is False:
        output("Resource package path doesn't exist", OutputType.ERROR)
        return

    output(f"Package pubspec path: {package_pubspec}", OutputType.INFO)
    if package_pubspec.exists() is False:
        output("Resource package pubspec doesn't exist", OutputType.ERROR)
        return

    # install flutter localization
    try:
        subprocess.run(
            ["flutter", "pub", "add", "flutter_localizations", "--sdk=flutter"],
            check=True,
            cwd=package_path,
            capture_output=False,
        )
        output("Added flutter_localizations package", OutputType.SUCCESS)
    except subprocess.CalledProcessError:
        output("Failed to add flutter_localizations package", OutputType.ERROR)
        return

    # Install intl package
    add_package(pub_path=package_path, package_name="intl", is_dev=False)

    # create arb files
    arb_folder = package_path / "lib" / "l10n"
    if arb_folder.exists():
        output("Localization folder already exists", OutputType.INFO)
        return
    arb_folder.mkdir(parents=True, exist_ok=True)
    arb_file_en = arb_folder / "app_en.arb"
    arb_file_np = arb_folder / "app_ne.arb"
    with arb_file_en.open("w") as f:
        json.dump(en_arb_content, f, ensure_ascii=False, indent=2)
    with arb_file_np.open("w") as f:
        json.dump(np_arb_content, f, ensure_ascii=False, indent=2)

    output("Created the ARB files", OutputType.SUCCESS)

    # Creating the l10n yaml file for package
    create_l10n_yaml(path=package_path, is_res=True, res_package=package_name)


    # Createing l10n yaml for apps 
    for app in apps:
        app_path = root_path / "apps" / app
        create_l10n_yaml(path=app_path, is_res=False, res_package=package_name)




