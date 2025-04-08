import configparser
from threading import Lock
from pathlib import Path
import io


class Config:
    def __init__(self, config_path='config.ini'):
        self.config_path = Path(config_path)
        self.lock = Lock()
        self.config = configparser.ConfigParser()
        self.reload()

    def reload(self):
        with self.lock:
            processed_content = self._remove_comments_from_config()
            self.config.read_file(io.StringIO(processed_content))

    def _remove_comments_from_config(self):
        with open(self.config_path, 'r') as file:
            lines = file.readlines()

        processed_lines = []
        for line in lines:
            # Strip leading/trailing whitespace and ignore empty lines or lines starting with ';'
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith(';;'):
                # Remove inline comments (anything after ';')
                comment_index = stripped_line.find(';;')
                if comment_index != -1:
                    stripped_line = stripped_line[:comment_index].strip()
                processed_lines.append(stripped_line)

        return '\n'.join(processed_lines)

    def get(self, key):
        with self.lock:
            category, key = self._parse_key(key)
            if category not in self.config:
                raise KeyError(f"Category '{category}' not found.")
            value = self.config[category][key]
            # Try to determine the correct type
            lower_val = value.lower()
            if lower_val in ('true', 'false'):
                return lower_val == 'true'
            elif value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                return value

    def set(self, key, value):
        with self.lock:
            category, key = self._parse_key(key)
            # Convert value to string representation
            if isinstance(value, bool):
                str_value = 'true' if value else 'false'
            else:
                str_value = str(value)
            if category not in self.config:
                self.config.add_section(category)
            self.config[category][key] = str_value
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

    @staticmethod
    def _parse_key(key):
        parts = key.split('.', 1)
        if len(parts) != 2:
            raise ValueError("Key must be in the format '<category>.<key>'.")
        return parts


# Global configuration instance
config = Config()
