import os


def get_env(name: str) -> str:
    """
    Get a required environment variable.
    """

    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Required environment variable '{name}' is missing."
        )

    return value


ACCOUNT_NAME = get_env("ACCOUNT_NAME")
CLIENT_ID = get_env("CLIENT_ID")

ASSETS_CONTAINER = get_env("ASSETS_CONTAINER")
FINDINGS_CONTAINER = get_env("FINDINGS_CONTAINER")

SECURITY_ASSETS_FILE = os.getenv(
    "SECURITY_ASSETS_FILE",
    "security-assets.json"
)

SECURITY_PLATFORMS_FILE = os.getenv(
    "SECURITY_PLATFORMS_FILE",
    "security-platforms.json"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
).upper()