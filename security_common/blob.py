import json

from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

from .config import (
    ACCOUNT_NAME,
    CLIENT_ID
)

from .logger import get_logger


logger = get_logger("blob")


class BlobStorage:
    """
    Wrapper around Azure Blob Storage.
    """

    def __init__(self):

        credential = ManagedIdentityCredential(
            client_id=CLIENT_ID
        )

        account_url = (
            f"https://{ACCOUNT_NAME}.blob.core.windows.net"
        )

        self.client = BlobServiceClient(
            account_url=account_url,
            credential=credential
        )

        logger.info(
            "Connected to storage account '%s'",
            ACCOUNT_NAME
        )

    def download_text(
        self,
        container_name: str,
        blob_name: str
    ) -> str:

        logger.debug(
            "Downloading blob '%s/%s'",
            container_name,
            blob_name
        )

        blob_client = self.client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        return (
            blob_client
            .download_blob()
            .readall()
            .decode("utf-8")
        )

    def download_json(
        self,
        container_name: str,
        blob_name: str
    ) -> dict:

        content = self.download_text(
            container_name,
            blob_name
        )

        return json.loads(content)

    def download_file(
        self,
        container_name: str,
        blob_name: str,
        local_path: str
    ) -> None:

        logger.debug(
            "Downloading file '%s/%s' -> '%s'",
            container_name,
            blob_name,
            local_path
        )

        blob_client = self.client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        with open(local_path, "wb") as file_handle:

            file_handle.write(
                blob_client.download_blob().readall()
            )

    def upload_file(
        self,
        container_name: str,
        blob_name: str,
        local_path: str
    ) -> None:

        logger.debug(
            "Uploading file '%s' -> '%s/%s'",
            local_path,
            container_name,
            blob_name
        )

        blob_client = self.client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        with open(local_path, "rb") as file_handle:

            blob_client.upload_blob(
                file_handle,
                overwrite=True
            )
            
    def upload_json(
        self,
        container_name: str,
        blob_name: str,
        data: dict | list
    ) -> None:

        logger.debug(
            "Uploading JSON to '%s/%s'",
            container_name,
            blob_name
        )

        blob_client = self.client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        blob_client.upload_blob(
            json.dumps(
                data,
                indent=2,
                sort_keys=True
            ),
            overwrite=True
        )