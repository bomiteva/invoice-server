import os
import shutil
import time
from pydantic import BaseModel
from starlette.datastructures import UploadFile


# data object for invoice file
class InvoiceFile(BaseModel):
    name: str
    dir: str
    timestamp: int


class UploadInvoiceFile:
    """Class creates base dir and uploads invoice file"""
    def __init__(self, upload_file: UploadFile, base_dir: str, timestamp: int = int(time.time())):
        self.upload_file = upload_file
        self.filename = upload_file.filename
        self.base_dir = base_dir
        self.timestamp = timestamp

    def save_upload_file(self) -> InvoiceFile:
        """Creates unique directory based on a timestamp and save the invoice in it."""
        file_dir = f"{self.base_dir}/invoices_{str(self.timestamp)}"
        file_path = file_dir + "/" + self.filename
        try:
            # creates file directory
            self.create_file_dir(file_dir)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(self.upload_file.file, buffer)
        finally:
            self.upload_file.file.close()
        # return data object with invoice file information
        return InvoiceFile(name=self.filename, dir=file_dir, timestamp=self.timestamp)

    @staticmethod
    def create_file_dir(file_dir: str) -> None:
        os.makedirs(file_dir, exist_ok=True)
