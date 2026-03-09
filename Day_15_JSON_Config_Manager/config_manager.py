import json
import os
import re
from typing import Any, Dict, Optional, Union

class ConfigManager:
    """
    A professional JSON configuration manager with support for:
    - Hierarchical access using dot notation (e.g., 'database.host')
    - Environment variable overrides (e.g., APP_DATABASE_HOST)
    - Type validation and default values
    - Recursive merging of configuration files
    """

    def __init__(self, prefix: str = "APP"):
        self._config: Dict[str, Any] = {}
        self._prefix = prefix.upper()

    def load_file(self, file_path: str) -> None:
        """Load configuration from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            self._config = self._merge(self._config, data)

    def _merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two dictionaries."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._merge(base[key], value)
            else:
                base[key] = value
        return base

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        Priority: Environment Variable > Loaded Config > Default
        """
        # 1. Check environment variable first
        env_key = f"{self._prefix}_{key_path.replace('.', '_').upper()}"
        if env_key in os.environ:
            return self._cast_env_value(os.environ[env_key])

        # 2. Navigate through the loaded config
        keys = key_path.split('.')
        value = self._config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def _cast_env_value(self, value: str) -> Any:
        """Attempt to cast environment variable string to appropriate type."""
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        if value.lower() == 'null' or value.lower() == 'none':
            return None
        
        # Try numeric types
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def set(self, key_path: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key_path.split('.')
        target = self._config
        for key in keys[:-1]:
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value

    def save(self, file_path: str) -> None:
        """Save the current configuration to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self._config, f, indent=4)

    def __repr__(self) -> str:
        return json.dumps(self._config, indent=2)


if __name__ == "__main__":
    # Example usage and demonstration
    print("--- JSON Config Manager Demo ---")
    
    # 1. Initialize
    cm = ConfigManager(prefix="MYAPP")
    
    # 2. Set some defaults
    cm.set("server.port", 8080)
    cm.set("server.host", "localhost")
    cm.set("database.enabled", True)
    
    print(f"Initial Config:\n{cm}")
    
    # 3. Demonstrate dot notation access
    print(f"\nAccessing 'server.port': {cm.get('server.port')}")
    
    # 4. Demonstrate Environment Variable Override
    os.environ["MYAPP_SERVER_PORT"] = "9090"
    print(f"Accessing 'server.port' after ENV override (MYAPP_SERVER_PORT=9090): {cm.get('server.port')}")
    
    # 5. Demonstrate Hierarchical ENV Override
    os.environ["MYAPP_DATABASE_ENABLED"] = "false"
    print(f"Accessing 'database.enabled' after ENV override (MYAPP_DATABASE_ENABLED=false): {cm.get('database.enabled')}")
    
    # 6. Save and Load simulation
    temp_file = "config_test.json"
    cm.save(temp_file)
    print(f"\nConfig saved to {temp_file}")
    
    new_cm = ConfigManager()
    new_cm.load_file(temp_file)
    print(f"Loaded config from file:\n{new_cm}")
    
    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
