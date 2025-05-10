import shutil
import subprocess
from pathlib import Path
from typing import List

from src.output_util import OutputType, output


def is_melos_installed() -> bool:
    """
    Check if Melos is globally installed and available in PATH.

    Returns:
        True if melos is available and working, False otherwise.
    """
    if shutil.which("melos") is None:
        return False

    try:
        subprocess.run(
            ["melos", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def activate_melos() -> bool:
    """
    Activates Melos globally using Dart if it is not already installed.

    Returns:
        True if Melos is successfully activated or already present, False otherwise.
    """
    output("Checking if Melos is installed...", OutputType.INFO)

    try:
        subprocess.run(["dart", "pub", "global", "activate", "melos"], check=True)
        output("Melos has been activated globally.", OutputType.SUCCESS)
        return True
    except subprocess.CalledProcessError as e:
        output("Failed to activate Melos.", OutputType.ERROR)
        output(f"Error: {e}", OutputType.ERROR)
        return False
    except FileNotFoundError:
        output(
            "Dart SDK not found. Make sure Dart is installed and in your PATH.",
            OutputType.ERROR,
        )
        return False


def melos_command(path: Path, commands: List[str]):
    output("Running melos commands", OutputType.INFO)
    try:
        subprocess.run(["melos", *commands], check=True, cwd=path)
        output("Melos command executed successfully.", OutputType.SUCCESS)
        return True
    except subprocess.CalledProcessError as e:
        output("Failed to run Melos command.", OutputType.ERROR)
        output(f"Error: {e}", OutputType.ERROR)
        return False
    except FileNotFoundError:
        output(
            "Dart SDK not found. Make sure Dart is installed and in your PATH.",
            OutputType.ERROR,
        )
        return False
