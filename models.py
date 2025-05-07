from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserInput:
    """
    class to pass user input
    """

    project_name: Optional[str]
    apps: List[str]
    packages: List[str]
