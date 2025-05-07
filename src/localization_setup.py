import json
import subprocess
from pathlib import Path

from src.package_util import add_package
from yaml_util import create_l10n_yaml

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


def setup_localization(package_name: str, root_path: Path):

    package_pubspec = root_path / package_name / "pubspec.yaml"
    package_path = root_path / package_name

    # install flutter localization
    try:
        subprocess.run(
            ["flutter", "pub", "get", "flutter_localization", "--sdk=flutter"],
            check=True,
            cwd=package_path,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        print("Failed to add localization")

    # Install intl package
    add_package(pub_path=package_path, package_name="intl", is_dev=False)

    # create arb files
    arb_folder = package_path / "lib" / "l10n"
    if arb_folder.exists():
        return
    arb_folder.mkdir(parents=True, exist_ok=True)
    arb_file_en = arb_folder / "intl_es.arb"
    arb_file_np = arb_folder / "intl_np.arb"
    with arb_file_en.open("w") as f:
        json.dump(en_arb_content, f, ensure_ascii=False, indent=2)

    print("Created the arb files")

    # Creating the l10n yaml file
    create_l10n_yaml(path=package_path, is_res=True, res_package=package_name)
    create_l10n_yaml(path=package_path, is_res=False, res_package=package_name)
