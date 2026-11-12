from datetime import datetime
from pathlib import Path

from .blob import BlobStorage
from .config import FINDINGS_CONTAINER

from .logger import get_logger


logger = get_logger("findings")


class FindingsManager:

    def __init__(self):

        self.storage = BlobStorage()

    def upload_latest(
        self,
        scanner_name: str,
        local_file: str
    ) -> None:

        blob_name = (
            f"{scanner_name}/latest.json"
        )

        logger.info(
            "Uploading latest findings for '%s'",
            scanner_name
        )

        self.storage.upload_file(
            FINDINGS_CONTAINER,
            blob_name,
            local_file
        )

    def upload_archive(
        self,
        scanner_name: str,
        local_file: str
    ) -> None:

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d-%H%M%S"
        )

        filename = Path(
            local_file
        ).name

        blob_name = (
            f"{scanner_name}/archive/"
            f"{timestamp}-{filename}"
        )

        logger.info(
            "Archiving findings for '%s'",
            scanner_name
        )

        self.storage.upload_file(
            FINDINGS_CONTAINER,
            blob_name,
            local_file
        )

    def upload_json(
        self,
        scanner_name: str,
        data: dict | list
    ) -> None:

        logger.info(
            "Uploading JSON findings for '%s'",
            scanner_name
        )

        blob_name = (
            f"{scanner_name}/latest.json"
        )

        self.storage.upload_json(
            FINDINGS_CONTAINER,
            blob_name,
            data
        )

    def download_latest(
        self,
        scanner_name: str
    ) -> dict | list:

        blob_name = (
            f"{scanner_name}/latest.json"
        )

        logger.info(
            "Downloading latest findings for '%s'",
            scanner_name
        )

        return self.storage.download_json(
            FINDINGS_CONTAINER,
            blob_name
        )