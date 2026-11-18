import re
import unicodedata

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

    def _generate_asset_id(
        self,
        value: str
    ) -> str:
        """
        Generate a stable asset ID.
        """

        value = unicodedata.normalize(
            "NFKD",
            value
        )

        value = value.encode(
            "ascii",
            "ignore"
        ).decode(
            "ascii"
        )

        value = value.lower()

        value = re.sub(
            r"^https?://",
            "",
            value
        )

        value = re.sub(
            r"[^a-z0-9]+",
            "-",
            value
        )

        return value.strip("-")

    def _normalize_assets(
        self,
        assets: list
    ) -> list:
        """
        Normalize assets and ensure unique IDs.
        """

        used_ids = set()

        normalized_assets = []

        for asset in assets:

            asset = dict(asset)

            asset_id = asset.get("id")

            if not asset_id:

                source_value = (
                    asset.get("url")
                    or asset.get("title")
                    or "unknown"
                )

                asset_id = (
                    self._generate_asset_id(
                        source_value
                    )
                )

            original_id = asset_id

            counter = 2

            while asset_id in used_ids:

                asset_id = (
                    f"{original_id}-{counter}"
                )

                counter += 1

            asset["id"] = asset_id

            used_ids.add(
                asset_id
            )

            normalized_assets.append(
                asset
            )

        return normalized_assets

    def get_assets(
        self
    ) -> list:

        logger.info(
            "Loading assets from '%s'",
            SECURITY_ASSETS_FILE
        )

        assets = (
            self.storage.download_json(
                ASSETS_CONTAINER,
                SECURITY_ASSETS_FILE
            )
        )

        normalized_assets = (
            self._normalize_assets(
                assets
            )
        )

        logger.info(
            "Loaded %s assets",
            len(normalized_assets)
        )

        return normalized_assets

    def get_platforms(
        self
    ) -> dict:

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

        platforms = (
            self.get_platforms()
        )

        result = []

        for asset in assets:

            if not asset.get(
                "active",
                False
            ):
                continue

            platform_name = (
                asset.get(
                    "platform",
                    ""
                )
                .strip()
                .lower()
            )

            platform = (
                platforms.get(
                    platform_name,
                    {}
                )
            )

            if platform.get(
                scanner_name,
                False
            ):
                result.append(
                    asset
                )

        logger.info(
            "Matched %s assets for scanner '%s'",
            len(result),
            scanner_name
        )

        return result