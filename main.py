import sys
from pathlib import Path

from input_util import take_user_input
from models import UserInput
from package_util import add_package, create_flutter_templates
from yaml_util import add_to_workspace, create_root_molos_yaml, create_root_pubspec_yaml


def main():
    """
    Entry point
    """
    print("Flutter monorepo setup:")
    # if len(sys.argv) < 2:
    #     sys.exit(" Usage: python main.py <project_name>")
    # project_name = sys.argv[1]
    # monorepo_path = Path.cwd() / project_name
    #
    # try:
    #     monorepo_path.mkdir(parents=True, exist_ok=False)
    # except FileExistsError:
    #     sys.exit(f" Folder '{project_name}' already exists.")
    #
    # print(f"📁 Created folder: {monorepo_path}")
    # create_root_pubspec_yaml(monorepo_path, project_name)
    # add_package(monorepo_path, "melos", True)

    # create_root_molos_yaml(monorepo_path, project_name)
    # create_flutter_templates(monorepo_path, ["hello_world"], True)
    # create_flutter_templates(monorepo_path, ["world_flutter"], False)
    # add_to_workspace(monorepo_path, ["hello_world"], ["world_flutter"])
    input = take_user_input()
    print(input)


if __name__ == "__main__":
    main()
