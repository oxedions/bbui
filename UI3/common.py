def write_custom_format(data: dict, filename: str):
    """Write dictionary to a custom file format with [key] headers and list values line by line. (INI like)"""
    with open(filename, 'w') as file:
        for key, values in data.items():
            file.write(f'[{key}]\n')
            for value in values:
                file.write(f'{value}\n')

def read_custom_format(filename: str) -> dict:
    """Read a custom formatted file (INI like) into a dictionary."""
    result = {}
    current_key = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('[') and line.endswith(']'):
                current_key = line[1:-1]
                result[current_key] = []
            elif current_key is not None:
                result[current_key].append(line)
            else:
                raise ValueError(f"Value without section header found: {line}")
    
    return result