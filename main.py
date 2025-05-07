import sys
from pathlib import Path

from src.input_util import take_user_input
from src.localization_setup import setup_localization
from src.package_util import add_package, create_flutter_templates
from src.yaml_util import (
    add_to_workspace,
    create_root_molos_yaml,
    create_root_pubspec_yaml,
)

sys.path.append(str(Path(__file__).resolve().parent))


def main():
    """
    Entry point
    """
    print("Flutter monorepo setup:")
    input = take_user_input()
    project_name = input.project_name
    if project_name is None:
        return
    monorepo_path = Path.cwd() / project_name
    try:
        monorepo_path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        sys.exit(f" Folder '{project_name}' already exists.")

    print(f"📁 Created folder: {monorepo_path}")
    create_root_pubspec_yaml(monorepo_path, project_name)
    add_package(monorepo_path, "melos", True)
    create_root_molos_yaml(monorepo_path, project_name)
    create_flutter_templates(monorepo_path, input.apps, is_app=True)
    create_flutter_templates(monorepo_path, input.packages, is_app=False)
    add_to_workspace(monorepo_path, input.apps, input.packages)
    res_package = project_name + "_resources"
    setup_localization(res_package, monorepo_path)


if __name__ == "__main__":
    main()
