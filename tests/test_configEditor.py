from multiSourceWordMaps.configEditor import ConfigEditor
from unittest.mock import patch
import os
import unittest
from mock_args import MockArgs

class TestConfigEditor(unittest.TestCase):

    def setUp(self):
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/test_data/config.py", 'w+') as config:
            config.write('{"package_dir": "", "sources": { }}')
        self.dist_dir = f"{os.path.dirname(os.path.abspath(__file__))}/test_data"
        self.data_dir = f"{os.path.dirname(os.path.abspath(__file__))}/test_data"
        return

    def tearDown(self):
       os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/test_data/config.py")
       return

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_file_not_found_on_init(self, mock_get_dist_dir, mock_get_data_dir):
        dist_dir = "not/real/file.py"
        mock_get_dist_dir.return_value = dist_dir
        mock_get_data_dir.return_value = self.data_dir
        with self.assertRaises(FileNotFoundError):
            ConfigEditor()
   
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_add_without_location_pdf(self, mock_get_dist_dir, mock_get_data_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_pdf(self, mock_get_dist_dir, mock_get_data_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","testFile.pdf",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]
        assert os.path.exists(f"{self.dist_dir}/PDFs/SQ/testFile.pdf")
        os.remove(f"{self.dist_dir}/PDFs/SQ/testFile.pdf")
        os.rmdir(f"{self.dist_dir}/PDFs/SQ")
        os.rmdir(f"{self.dist_dir}/PDFs")

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_website(self, mock_get_dist_dir, mock_get_data_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","https://www.google.com",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        with self.assertRaises(BaseException):
            configEditor.add_to_config(args)

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_website_file_not_found(self, mock_get_dist_dir, mock_get_data_dir):
        args = MockArgs("SQ","testFile.pdf","DummyLocation")
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        with self.assertRaises(FileNotFoundError):
            configEditor.add_to_config(args)

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_remove_not_in_sources(self, mock_get_dist_dir, mock_get_data_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        with self.assertRaises(BaseException):
            configEditor.remove_from_config(args)
        configEditor.add_to_config(args)
        configEditor.config["sources"] = {"SQ":[]}
        with self.assertRaises(BaseException):
            configEditor.remove_from_config(args)

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_remove(self, mock_get_dist_dir, mock_get_data_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","testFile.pdf",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        configEditor.add_to_config(args)
        configEditor.remove_from_config(args)
        assert configEditor.config["sources"] == {}
        assert not os.path.exists(f"{self.dist_dir}/PDFs/SQ")
        os.rmdir(f"{self.dist_dir}/PDFs")

    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_data_dir")
    @patch("multiSourceWordMaps.configEditor.ConfigEditor.get_dist_dir")
    def test_list(self, mock_get_dist_dir, mock_get_data_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        mock_get_data_dir.return_value = self.data_dir
        configEditor = ConfigEditor()
        configEditor.add_to_config(args)
        configEditor.list_config()
        assert True


