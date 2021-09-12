import base64
from xml.etree.ElementTree import Element, ElementTree, SubElement

import numpy as np
import pandas
from pandas import DataFrame

from app.errors import InvalidParamsError
from app.upload_invoice_file import InvoiceFile


class ProcessInvoiceFile:
    """Class that processes invoices, saves csv, xml and image in the InvoiceFile directory"""
    def __init__(self, invoice_file: InvoiceFile):
        self.invoice_file = invoice_file

    def process_file(self):
        """Process InvoiceFile object - using pandas library for easier processing"""
        # read DataFrame
        data = pandas.read_csv(self.invoice_file.dir + "/" + self.invoice_file.name)

        if "buyer" in data:
            # group by buyer - like sql statement
            for buyer, group in data.groupby(["buyer"]):
                # create all cvs files
                group.to_csv(f"{self.invoice_file.dir}/{buyer}.csv", index=False)
                # create all xml files
                self._process_xml(buyer, group)
        else:
            raise InvalidParamsError(message="Missing buyer in file")

    def _process_xml(self, buyer: str, group: DataFrame) -> ElementTree:
        """Creates xml file with same csv format."""
        # replace all nan with empty str
        data_group = group.replace(np.nan, "", regex=True)

        xml_root = Element("root")
        xml_tree = ElementTree(xml_root)
        # iterate over all rows
        for _, row in data_group.iterrows():
            xml_invoice = Element("invoice")
            for k, v in row.items():
                if k == "invoice_image":
                    if v != "":  # save image only for existing data
                        self._save_image(row["image_name"], row["invoice_image"])
                    continue
                xml_element = SubElement(xml_invoice, str(k))
                xml_element.text = str(v)

            xml_root.append(xml_invoice)
        # save xml file in the same invoice directory
        xml_tree.write(f"{self.invoice_file.dir}/{buyer}.xml")
        return xml_tree

    def _save_image(self, img_name: str, img_data: str):
        """Saves decoded image."""
        with open(f"{self.invoice_file.dir}/{img_name}", "wb") as file_handler:
            file_handler.write(base64.b64decode(img_data))

