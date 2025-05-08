import sys
from pathlib import Path

from src.input_util import take_user_input
from src.localization_setup import setup_localization
from src.package_util import add_package, create_flutter_templates
from src.yaml import add_to_workspace, create_root_melos_yaml, create_root_pubspec_yaml
from src.output_util import output, OutputType


def main():
    """
    Entry point
    """
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
        sys.exit()

    output(f"Created folder: {monorepo_path}", OutputType.SUCCESS)
    create_root_pubspec_yaml(monorepo_path, project_name)
    add_package(monorepo_path, "melos", True)
    create_root_melos_yaml(monorepo_path, project_name)
    create_flutter_templates(monorepo_path, input.apps, is_app=True)
    create_flutter_templates(monorepo_path, input.packages, is_app=False)
    add_to_workspace(monorepo_path, input.apps, input.packages)
    res_package = project_name + "_resources"
    setup_localization(res_package, monorepo_path, input.apps)


if __name__ == "__main__":
    main()
