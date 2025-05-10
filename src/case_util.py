import re
def snake_to_pascal(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components if x)

def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    pascal = snake_to_pascal(snake_str)
    return pascal[0].lower() + pascal[1:] if pascal else ''

def pascal_to_snake(pascal_str: str) -> str:
    """Convert PascalCase (or camelCase) to snake_case."""
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str).lower()
    return snake

def camel_to_snake(camel_str: str) -> str:
    """Convert camelCase to snake_case."""
    return pascal_to_snake(camel_str)

def pascal_to_camel(pascal_str: str) -> str:
    """Convert PascalCase to camelCase."""
    return pascal_str[0].lower() + pascal_str[1:] if pascal_str else ''

def camel_to_pascal(camel_str: str) -> str:
    """Convert camelCase to PascalCase."""
    return camel_str[0].upper() + camel_str[1:] if camel_str else ''
