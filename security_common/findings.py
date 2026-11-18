import json

from datetime import datetime
from pathlib import Path

from .blob import BlobStorage
from .config import FINDINGS_CONTAINER
from .logger import get_logger

logger = get_logger("findings")


class FindingsManager:

    def __init__(self):
        self.storage = BlobStorage()

    def create_result(
        self,
        scanner_name: str,
        targets: int,
        findings: list
    ) -> dict:
        """
        Create a standardized result structure
        used by all scanners.
        """

        severity_count = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        for finding in findings:

            severity = (
                finding.get(
                    "severity",
                    "info"
                )
                .lower()
            )

            if severity in severity_count:
                severity_count[
                    severity
                ] += 1

        return {
            "scanner": scanner_name,
            "status": "SUCCESS",
            "timestamp": (
                datetime.utcnow().isoformat()
                + "Z"
            ),
            "summary": {
                "targets": targets,
                "findings": len(findings),
                **severity_count
            },
            "findings": findings
        }

    def create_empty_result(
        self,
        scanner_name: str,
        targets: int = 0
    ) -> dict:
        """
        Create an empty standardized result.
        """

        return {
            "scanner": scanner_name,
            "status": "SUCCESS",
            "timestamp": (
                datetime.utcnow().isoformat()
                + "Z"
            ),
            "summary": {
                "targets": targets,
                "findings": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            },
            "findings": []
        }

    def save_result_file(
        self,
        local_file: str,
        result: dict
    ) -> None:
        """
        Save a standardized result object
        to a local JSON file.
        """

        with open(
            local_file,
            "w",
            encoding="utf-8"
        ) as file_handle:

            json.dump(
                result,
                file_handle,
                indent=2
            )

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

    def publish(
        self,
        scanner_name: str,
        local_file: str
    ) -> None:
        """
        Publish findings by updating latest
        and creating an archive copy.
        """

        logger.info(
            "Publishing findings for '%s'",
            scanner_name
        )

        self.upload_latest(
            scanner_name,
            local_file
        )

        self.upload_archive(
            scanner_name,
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