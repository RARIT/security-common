from .blob import BlobStorage
from .config import (
    ASSETS_CONTAINER,
    SECURITY_ASSETS_FILE,
    SECURITY_PLATFORMS_FILE
)

from .logger import get_logger


logger = get_logger("assets")


class AssetManager:

    def __init__(self):

        self.storage = BlobStorage()

    def get_assets(self) -> list:

        logger.info(
            "Loading assets from '%s'",
            SECURITY_ASSETS_FILE
        )

        return self.storage.download_json(
            ASSETS_CONTAINER,
            SECURITY_ASSETS_FILE
        )

    def get_platforms(self) -> list:

        logger.info(
            "Loading platforms from '%s'",
            SECURITY_PLATFORMS_FILE
        )

        return self.storage.download_json(
            ASSETS_CONTAINER,
            SECURITY_PLATFORMS_FILE
        )
        
    def get_assets_for_scanner(
        self,
        scanner_name: str
    ) -> list:

        assets = self.get_assets()
        platforms = self.get_platforms()

        logger.info("Assets: %s", assets)
        logger.info("Platforms: %s", platforms)

        result = []

        for asset in assets:

            logger.info("Asset: %s", asset)

            logger.info(
                "active=%s",
                asset.get("active")
            )

            logger.info(
                "platform=%s",
                asset.get("platform")
            )

            platform_name = (
                asset.get("platform", "")
                .strip()
                .lower()
            )

            platform = platforms.get(
                platform_name,
                {}
            )

            logger.info(
                "platform config=%s",
                platform
            )

            logger.info(
                "scanner enabled=%s",
                platform.get(scanner_name, False)
            )

            if platform.get(scanner_name, False):
                result.append(asset)

        logger.info(
            "Matched assets count: %s",
            len(result)
        )

        return result