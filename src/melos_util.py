import shutil
import subprocess


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
    print("🔍 Checking if Melos is installed...")

    try:
        subprocess.run(["dart", "pub", "global", "activate", "melos"], check=True)
        print(" Melos has been activated globally.")
        return True
    except subprocess.CalledProcessError as e:
        print(" Failed to activate Melos.")
        print(f" Error: {e}")
        return False
    except FileNotFoundError:
        print(" Dart SDK not found. Make sure Dart is installed and in your PATH.")
        return False
