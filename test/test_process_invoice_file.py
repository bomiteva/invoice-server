import base64
import unittest
from unittest.mock import patch, call, mock_open

import pandas
from pandas import Series

from app.errors import InvalidParamsError
from app.process_invoice_file import ProcessInvoiceFile
from app.upload_invoice_file import InvoiceFile


class ProcessInvoiceFileTest(unittest.TestCase):
    """Unit tests for ProcessInvoiceFile class"""
    def setUp(self) -> None:
        self.invoice_file = InvoiceFile(name="test.csv", dir=".", timestamp=1631351454)
        self.process = ProcessInvoiceFile(self.invoice_file)

    @patch('xml.etree.ElementTree.ElementTree.write')
    @patch('pandas.DataFrame.to_csv')
    @patch('pandas.read_csv')
    def test_process_file_without_encode_img(self, mock_read_csv, mock_to_csv, mock_write_xml):
        """Tests creation of xml and csv files without image data."""
        mock_read_csv.return_value = pandas.DataFrame({'buyer': Series(["South African Gold Mines Corp",
                                                                        "South African Gold Mines Corp", "Traksas"]),
                                                       'image_name': Series(
                                                           ["scanned_invoice_1.png", "", "scanned_invoice_3.png"])})
        # invoke function
        self.process.process_file()

        # assert csv creation calls
        mock_to_csv.assert_has_calls(
            [call('./South African Gold Mines Corp.csv', index=False),
             call('./Traksas.csv', index=False)])

        # assert xml creation calls
        mock_write_xml.assert_has_calls(
            [call('./South African Gold Mines Corp.xml'),
             call('./Traksas.xml')])

    @patch('builtins.open', new_callable=mock_open)
    @patch('xml.etree.ElementTree.ElementTree.write')
    @patch('pandas.DataFrame.to_csv')
    @patch('pandas.read_csv')
    def test_process_file_with_encode_img(self, mock_read_csv, mock_to_csv, mock_write_xml, mock_img_handler):
        """Tests creation of xml and csv files with encoded image data."""
        mock_read_csv.return_value = pandas.DataFrame({'buyer': Series(["South African Gold Mines Corp",
                                                                        "South African Gold Mines Corp", "Traksas"]),
                                                       'image_name': Series(
                                                           ["scanned_invoice_1.png", "", "scanned_invoice_3.png"]),
                                                       'invoice_image': Series([
                                                           "iVBORw0KGgoAAAANSUhEUgAABAcAAACECAYAAADsr0InAAAKuGlDQ1BJQ0MgUHJvZmlsZQAASImVlgdUU1kax+97L70AIYCAlNCbIJ0AUkIPvTcbIQkklBgTgopdEUdgRBERwTKgIoiCo1JkLIgFK4oF7AMiKuo4WLChsg9Ywszu2d2z3zk395cv3/3Ky7vn/AGgfOOIxRmwEgCZoixJpL8XIz4hkYF/CiAAAzKwBRCHKxWzwsODAWqT+9/tYzcajdoty7Fc//77fzUajy/lAgCFo5zMk3IzUT6GrqdcsSQLAKQM9RssyhKP8QmUVSRogyjfGOPUCX46xskT/Hk8JjrSGwAMBQAChcORpAJAUUf9jGxuKpqHwkTZWsQTilAWoOzOFXB4KNegPCMzc8EY30bZNPkveVL/ljNZnpPDSZXzxCzjRvARSsUZnCX/5+P435aZIZusYQzGBpAERI7t6DO7m74gSM6i5NCwSRbyxuPHWSALiJlkrtQ7cZJ5HJ8g+dmM0OBJThH6seV5stjRk8yX+kZNsmRBpLxWisSbNckcyVRdWXqM3C/gs+X5cwTRcZOcLYwNnWRpelTQVIy33C+RRcr754v8vabq+slnz5T+ZV4hW342SxAdIJ+dM9U/X8SayimNl/fG4/v4TsXEyOPFWV7yWuKMcHk8P8Nf7pdmR8nPZqEv5NTZcPkzTOMEhk8yCEJvmz26AkBwFn9x1tgA3gvESyTCVEEWg4XeLD6DLeJazWDYWttaAzB2Tydeg/fXx+8fpJ485ctAe3KiAQCfnvJx3QBoRP8npcopn0kIAPRKAE5f48ok2RM+zNgHFpCAIlABGkAHGABTYIl25ghcgSfwBYEgDESDBDAPcIEAZAIJWASWgdUgDxSATWArKAe7wR5QAw6BI6AZnABnwAVwBdwAd8AD0AsGwCswBD6CEQiC8BAVokMakC5kBFlAthATcod8oWAoEkqAkqBUSATJoGXQWqgAKobKoUqoFvoVOg6dgS5BXdA9qA8ahN5BX2EEpsAqsDZsDM+EmTALDoKj4blwKrwQzoFz4Y1wGVwFH4Sb4DPwFfgO3Au/",
                                                           "",
                                                           "iVBORw0KGgoAAAANSUhEUgAABAcAAACECAYAAADsr0InAAAKuGlDQ1BJQ0MgUHJvZmlsZQAASImVlgdUU1kax+97L70AIYCAlNCbIJ0AUkIPvTcbIQkklBgTgopdEUdgRBERwTKgIoiCo1JkLIgFK4oF7AMiKuo4WLChsg9Ywszu2d2z3zk395cv3/3Ky7vn/AGgfOOIxRmwEgCZoixJpL8XIz4hkYF/CiAAAzKwBRCHKxWzwsODAWqT+9/tYzcajdoty7Fc//77fzUajy/lAgCFo5zMk3IzUT6GrqdcsSQLAKQM9RssyhKP8QmUVSRogyjfGOPUCX46xskT/Hk8JjrSGwAMBQAChcORpAJAUUf9jGxuKpqHwkTZWsQTilAWoOzOFXB4KNegPCMzc8EY30bZNPkveVL/ljNZnpPDSZXzxCzjRvARSsUZnCX/5+P435aZIZusYQzGBpAERI7t6DO7m74gSM6i5NCwSRbyxuPHWSALiJlkrtQ7cZJ5HJ8g+dmM0OBJThH6seV5stjRk8yX+kZNsmRBpLxWisSbNckcyVRdWXqM3C/gs+X5cwTRcZOcLYwNnWRpelTQVIy33C+RRcr754v8vabq+slnz5T+ZV4hW342SxAdIJ+dM9U/X8SayimNl/fG4/v4TsXEyOPFWV7yWuKMcHk8P8Nf7pdmR8nPZqEv5NTZcPkzTOMEhk8yCEJvmz26AkBwFn9x1tgA3gvESyTCVEEWg4XeLD6DLeJazWDYWttaAzB2Tydeg/fXx+8fpJ485ctAe3KiAQCfnvJx3QBoRP8npcopn0kIAPRKAE5f48ok2RM+zNgHFpCAIlABGkAHGABTYIl25ghcgSfwBYEgDESDBDAPcIEAZAIJWASWgdUgDxSATWArKAe7wR5QAw6BI6AZnABnwAVwBdwAd8AD0AsGwCswBD6CEQiC8BAVokMakC5kBFlAthATcod8oWAoEkqAkqBUSATJoGXQWqgAKobKoUqoFvoVOg6dgS5BXdA9qA8ahN5BX2EEpsAqsDZsDM+EmTALDoKj4blwKrwQzoFz4Y1wGVwFH4Sb4DPwFfgO3Au/"])})
        # invoke function
        self.process.process_file()

        # assert csv creation calls
        mock_to_csv.assert_has_calls(
            [call('./South African Gold Mines Corp.csv', index=False),
             call('./Traksas.csv', index=False)])

        # assert xml creation calls
        mock_write_xml.assert_has_calls(
            [call('./South African Gold Mines Corp.xml'),
             call('./Traksas.xml')])

        # assert img creation calls
        mock_img_handler.assert_any_call('./scanned_invoice_1.png', 'wb')
        mock_img_handler.assert_any_call('./scanned_invoice_3.png', 'wb')
        self.assertEqual(mock_img_handler().write.call_count, 2)

    @patch('pandas.read_csv')
    def test_process_file_without_buyer(self, mock_read_csv):
        """Tests if InvalidParamsError throws when buyer missing"""
        mock_read_csv.return_value = pandas.DataFrame({'image_name': Series(
                                                           ["scanned_invoice_1.png", "", "scanned_invoice_3.png"])})
        # assert if error is raises
        with self.assertRaises(InvalidParamsError):
            self.process.process_file()

    @patch('builtins.open', new_callable=mock_open)
    def test_save_img(self, mock_img_handler):
        """Tests save image encoded data."""
        test_file_path = "test/file/path"
        content = "iVBORw0KGgoAAAANSUhEUgAABAcAAACECAYAAADsr0InAAAKuGlDQ1BJQ0MgUHJvZmlsZQAASImVlgdUU1kax+97L70AIYCAlNCbIJ0AUkIPvTcbIQkklBgTgopdEUdgRBERwTKgIoiCo1JkLIgFK4oF7AMiKuo4WLChsg9Ywszu2d2z3zk395cv3/3Ky7vn/AGgfOOIxRmwEgCZoixJpL8XIz4hkYF/CiAAAzKwBRCHKxWzwsODAWqT+9/tYzcajdoty7Fc//77fzUajy/lAgCFo5zMk3IzUT6GrqdcsSQLAKQM9RssyhKP8QmUVSRogyjfGOPUCX46xskT/Hk8JjrSGwAMBQAChcORpAJAUUf9jGxuKpqHwkTZWsQTilAWoOzOFXB4KNegPCMzc8EY30bZNPkveVL/ljNZnpPDSZXzxCzjRvARSsUZnCX/5+P435aZIZusYQzGBpAERI7t6DO7m74gSM6i5NCwSRbyxuPHWSALiJlkrtQ7cZJ5HJ8g+dmM0OBJThH6seV5stjRk8yX+kZNsmRBpLxWisSbNckcyVRdWXqM3C/gs+X5cwTRcZOcLYwNnWRpelTQVIy33C+RRcr754v8vabq+slnz5T+ZV4hW342SxAdIJ+dM9U/X8SayimNl/fG4/v4TsXEyOPFWV7yWuKMcHk8P8Nf7pdmR8nPZqEv5NTZcPkzTOMEhk8yCEJvmz26AkBwFn9x1tgA3gvESyTCVEEWg4XeLD6DLeJazWDYWttaAzB2Tydeg/fXx+8fpJ485ctAe3KiAQCfnvJx3QBoRP8npcopn0kIAPRKAE5f48ok2RM+zNgHFpCAIlABGkAHGABTYIl25ghcgSfwBYEgDESDBDAPcIEAZAIJWASWgdUgDxSATWArKAe7wR5QAw6BI6AZnABnwAVwBdwAd8AD0AsGwCswBD6CEQiC8BAVokMakC5kBFlAthATcod8oWAoEkqAkqBUSATJoGXQWqgAKobKoUqoFvoVOg6dgS5BXdA9qA8ahN5BX2EEpsAqsDZsDM+EmTALDoKj4blwKrwQzoFz4Y1wGVwFH4Sb4DPwFfgO3Au/"

        self.process._save_image(test_file_path, content)

        # assert if opened file on write mode 'wb'
        mock_img_handler.assert_called_once_with(f"{self.process.invoice_file.dir}/{test_file_path}", 'wb')

        # assert if the specific content was written in file
        mock_img_handler().write.assert_called_once_with(base64.b64decode(content))
