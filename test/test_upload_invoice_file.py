import unittest
from unittest.mock import patch, mock_open

from fastapi import UploadFile

from app.upload_invoice_file import UploadInvoiceFile


class UploadInvoiceFileTest(unittest.TestCase):
    """Unit tests for UploadInvoiceFile class"""
    def setUp(self) -> None:
        self.invoice_file = UploadFile("test.csv")
        self.upload_invoice = UploadInvoiceFile(upload_file=self.invoice_file, base_dir=".", timestamp=1123345555)

    @patch('os.makedirs')
    @patch('shutil.copyfileobj')
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_upload_file(self, mock_img_handler, mock_copy_object, mock_make_dir):
        """Tests """
        self.upload_invoice.save_upload_file()

        # assert if dir is created
        mock_make_dir.assert_called_once_with('./invoices_1123345555', exist_ok=True)

        # assert if opened file on write mode 'wb'
        mock_img_handler.assert_called_once_with('./invoices_1123345555/test.csv', 'wb')

        # assert if the specific content was written in file
        mock_copy_object.assert_called_once()
