from enum import Enum
from colorama import Fore, Style, init

# Initialize colorama
init()

class OutputType(Enum):
    ERROR = "❌"
    INFO = "ℹ️"
    SUCCESS = "✓"

def output(message: str, output_type: OutputType) -> None:
    """
    Output a message with appropriate color and tag based on the type.

    Args:
        message: The message to display
        output_type: The type of message (ERROR, INFO, or SUCCESS)
    """
    color = {
        OutputType.ERROR: Fore.RED,
        OutputType.INFO: Fore.BLUE,
        OutputType.SUCCESS: Fore.GREEN
    }[output_type]

    print(f"{color}{output_type.value} {message}{Style.RESET_ALL}")