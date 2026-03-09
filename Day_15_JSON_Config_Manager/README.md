# Day 15: JSON Config Manager

A hierarchical configuration system for Python applications that supports environment variable overrides, dot-notation access, and recursive merging of JSON configuration files.

## Features

- **Dot Notation Access**: Easily access nested configuration values (e.g., `config.get('database.host')`).
- **Environment Variable Overrides**: Override any configuration value using environment variables with a custom prefix (e.g., `APP_DATABASE_HOST`).
- **Recursive Merging**: Merge multiple configuration files or default values seamlessly.
- **Type Casting**: Automatically casts environment variable strings to their appropriate types (bool, int, float, or None).
- **File Persistence**: Load and save configurations to JSON files.

## Usage

```python
from config_manager import ConfigManager
import os

# Initialize with an optional prefix for environment variables
cm = ConfigManager(prefix="MYAPP")

# Set defaults
cm.set("server.port", 8080)
cm.set("database.host", "localhost")

# Override with environment variable
os.environ["MYAPP_SERVER_PORT"] = "9090"

# Access values
port = cm.get("server.port")  # Returns 9090 (int)
host = cm.get("database.host")  # Returns "localhost"

# Load from file
cm.load_file("config.json")

# Save to file
cm.save("new_config.json")
```

## How It Works

The `ConfigManager` prioritizes values in the following order:
1.  **Environment Variables**: If an environment variable matching the key path (e.g., `PREFIX_KEY_SUBKEY`) exists, it is used.
2.  **Loaded Configuration**: The values loaded from JSON files or set manually.
3.  **Default Value**: The default value provided to the `get()` method if no value is found.

## License
MIT License
