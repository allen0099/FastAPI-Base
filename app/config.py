import os
from ast import literal_eval
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

_configs: dict[str, Any] = {
    "DEBUG": False,
    "RELOAD": False,
}

BASE_FOLDER: Path = Path(__file__).parent.parent
LOG_FOLDER: Path = BASE_FOLDER / "logs"


class ValidateException(Exception):
    """
    The exception for the validation of the environment variables
    """

    pass


def __load() -> None:
    """
    Load the environment variables from the .env file or os environment variables.

    Returns:
        None
    """
    env_file: Path = BASE_FOLDER / ".env"

    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)


def __initialize() -> None:
    """
    Initialize the config, check if the environment variables are valid.

    Returns:

    """
    for directory in [LOG_FOLDER]:
        if not directory.exists():
            directory.mkdir(parents=True)


def __convert_bool(value: str) -> bool:
    """
    Convert the string value to boolean value

    Args:
        value: The string value

    Returns:
        bool: The boolean value
    """
    if value.lower() in ["true", "t", "1", "yes", "y", "on"]:
        return True

    elif value.lower() in ["false", "f", "0", "no", "n", "off"]:
        return False

    else:
        raise ValueError(f"Cannot convert {value} to boolean value.")


def __auto_convert(env: Any) -> Any:
    if isinstance(env, str):
        try:
            env = __convert_bool(env)

        except ValueError:
            try:
                # Auto guess type, only support int, float, list, dict
                env = literal_eval(env)

            except (ValueError, SyntaxError):
                pass
    elif env is None:
        env = None
    else:
        raise ValueError(f"Cannot convert {env}, should be a string.")

    return env


def get(key: str, default: Any = None, *, convert: bool = False, raise_error: bool = False) -> Any:
    """
    Get the value of the key from the config file, if not found, return the default value

    Args:
        key: The key of the config
        default: The default value if the key is not found
        convert: If the value should be converted to the correct type, otherwise, return the string type value
        raise_error: If the key is not found and the default value is None, raise the KeyError

    Returns:
        Any: The value of the key
    """
    env: Any = os.getenv(key)

    if convert:
        env = __auto_convert(env)

    if env is not None:
        return env

    if key in _configs and _configs[key] is not None:
        return _configs[key]

    else:
        if raise_error and default is None:
            raise KeyError(f"Key {key} not found.")

        return default


# Indirectly call the __load function
__load()
__initialize()

DEBUG: bool = get("DEBUG", False, convert=True)
RELOAD: bool = get("RELOAD", False, convert=True)
LOG_CONFIG: str = str(BASE_FOLDER / "logger.json")
