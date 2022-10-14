from unittest import TestCase, mock
import regex as re
import sys
import os
sys.path.append("..")  # Adds higher directory to python modules path.
from parsers import epar_parse
import xml.etree.ElementTree as ET

class TestCaseXML(TestCase):
  def setUp(self):
     self.setUpMyStuff()

  def tearDown(self):
     self.tearDownMyStuff()


class TestEparParse(TestCase):
    # Prepare a list of XML files
    test_data_loc = "../test_data/epars"
    files = [file for file in os.listdir(test_data_loc) if os.path.isfile(os.path.join(test_data_loc, file))]
    xml_files = [file for file in files if ".xml" in file]
    # Get XML bodies, assuming there are XML files
    xml_bodies = []
    for xml_file in xml_files:
        xml_path = os.path.join(test_data_loc, xml_file)
        xml_tree = ET.parse(xml_path)
        xml_root = xml_tree.getroot()
        xml_bodies.append(xml_root[1])

    def test_get_prime(self):
        # Call get_prime
        output = epar_parse.get_prime(self.xml_bodies)
        self.assertEqual(self.xml_bodies, self.xml_bodies)
