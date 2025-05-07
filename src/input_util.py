import re
from typing import List

from src.models import UserInput


def select_resouce_package(packages: List[str]) -> str:
    """
    Selects the resource package
    """
    return "hello"


def take_user_input() -> UserInput:
    """
    Takes the user input
        Takes the name of the project
        Takes the array of apps
        and the array of packages
    returns a dict of str and list[str]
    """
    while True:
        project_name = input("Enter the root project name:").strip()
        if project_name:
            res = validate_name_format(project_name)
            if res:
                break
        else:
            print("Project Name can't be empty")

    RES_PACKAGE = project_name + "_resources"
    COMP_PACKAGE = project_name + "_components"

    packages = [RES_PACKAGE, COMP_PACKAGE]
    # while True:
    #     print("Enter the packages:(seperated by a comma)")
    #     packages_str = input("Packages:")
    #     packages = (
    #         [package.strip() for package in packages_str.split(",")]
    #         if packages_str
    #         else []
    #     )
    #     are_pacakges_valid = validate_names(packages, packages_str)
    #     if are_pacakges_valid:
    #         break
    #
    while True:
        print("Enter the apps:(seperated by a comma)")
        apps_str = input("apps:")
        apps = [app.strip() for app in apps_str.split(",")] if apps_str else []

        are_apps_valid = validate_names(apps, project_name)

        are_pacakges_valid = validate_names(packages, project_name)

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
    if res is None:
        print(f"Invalid name for {name}")
        return False
    return True
