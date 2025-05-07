import re
from typing import List

from models import UserInput


def take_user_input() -> UserInput:
    """
    Takes the user input
        Takes the name of the project
        Takes the array of apps
        and the array of packages
    returns a dict of str and list[str]
    """
    while True:
        while True:
            project_name = input("Enter the root project name:").strip()
            if project_name:
                res = validate_name_format(project_name)
                if res:
                    break
            print("Project Name can't be empty")

        print("Enter the packages:(seperated by a comma)")
        packages_str = input("Packages:")
        packages = (
            [package.strip() for package in packages_str.split(",")]
            if packages_str
            else []
        )

        print("Enter the apps:(seperated by a comma)")
        apps_str = input("apps:")
        apps = [app.strip() for app in apps_str.split(",")] if apps_str else []
        are_pacakges_valid = validate_names(packages, packages_str)
        are_apps_valid = validate_names(apps, packages_str)

        if are_pacakges_valid and are_apps_valid:
            break

    return UserInput(project_name, apps, packages)


def validate_names(names: List[str], project_name: str) -> bool:
    """
    wrapper for multiple package/app names
    """
    if project_name in names:
        print(
            "Invalid package or app name.(package or app name cannot be same to the root project name)"
        )
        return False

    for name in names:
        if validate_name_format(name) is False:
            return False
    return True


def validate_name_format(name: str) -> bool:
    """
    Validates a single package name.

    Return a bool
        True if matches
        False if Doesn't

    """
    FLUTTER_PKG_REG = re.compile(r"^[a-z](?:[a-z0-9_]*[a-z0-9])?$")
    res = re.match(FLUTTER_PKG_REG, name)
    if res:
        print(f"Invalid name for {name}")
        return False
    return True
