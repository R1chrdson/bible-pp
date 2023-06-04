import os
from pathlib import Path
from typing import Union, get_type_hints

from dotenv import load_dotenv

load_dotenv()

class AppConfigError(Exception):
    """Raised when there is an error in the configuration"""


def _parse_bool(val: Union[str, bool]) -> bool:
    return val if isinstance(val, bool) else val.lower() in ["true", "yes", "1"]


class AppConfig:
    """
    General configuration class for the project
    Maps environment variables to class attributes
    """

    BIBLES_PATH: Path

    def __init__(self, env):
        for field in self.__annotations__:  # pylint: disable=no-member
            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError(f"The {field} field is required")

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError as err:
                raise AppConfigError(
                    f'Unable to cast value of "{env[field]}" to type "{var_type}" for "{field}" field'
                ) from err

    def __getitem__(self, key):
        return self.__getattribute__(key)

Config = AppConfig(os.environ)