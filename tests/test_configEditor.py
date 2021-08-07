from multiSourceWordMap.configEditor import ConfigEditor
from unittest.mock import patch
import os
import unittest

class TestConfigEditor(unittest.TestCase):

   
        

    def setUp(self):
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/test_data/config.py", 'w+') as config:
            config.write('{"package_dir": "", "sources": { }}')
        self.dist_dir = f"{os.path.dirname(os.path.abspath(__file__))}/test_data"
        return

    def tearDown(self):
       os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/test_data/config.py")
       return
    
    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_init_configEditor_package_dir(self, mock_get_dist_dir):
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor('test/path')
        config = configEditor.config
        assert os.path.exists(f"{self.dist_dir}/config.py")
        assert config["package_dir"] == 'test/path'
        assert "sources" in config
    
    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_init_configEditor_no_package_dir(self, mock_get_dist_dir):
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor()
        config = configEditor.config
        assert config["package_dir"] == ''
        assert "sources" in config

    
    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_file_not_found_on_init(self, mock_get_dist_dir):
        dist_dir = "not/real/file.py"
        mock_get_dist_dir.return_value = dist_dir
        with self.assertRaises(FileNotFoundError):
            ConfigEditor()
    
    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_add_without_location_pdf(self, mock_get_dist_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor()
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]

    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_pdf(self, mock_get_dist_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","testFile.pdf",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor(self.dist_dir)
        configEditor.add_to_config(args)
        assert configEditor.config["sources"]["SQ"] == ["testFile.pdf"]
        assert os.path.exists(f"{self.dist_dir}/PDFs/SQ/testFile.pdf")
        os.remove(f"{self.dist_dir}/PDFs/SQ/testFile.pdf")
        os.rmdir(f"{self.dist_dir}/PDFs/SQ")
        os.rmdir(f"{self.dist_dir}/PDFs")

    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_website(self, mock_get_dist_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","https://www.google.com",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor(self.dist_dir)
        with self.assertRaises(BaseException):
            configEditor.add_to_config(args)

    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_add_with_location_website_file_not_found(self, mock_get_dist_dir):
        args = MockArgs("SQ","testFile.pdf","DummyLocation")
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor(self.dist_dir)
        with self.assertRaises(FileNotFoundError):
            configEditor.add_to_config(args)

    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_remove_not_in_sources(self, mock_get_dist_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor()
        with self.assertRaises(BaseException):
            configEditor.remove_from_config(args)
        configEditor.add_to_config(args)
        configEditor.config["sources"] = {"SQ":[]}
        with self.assertRaises(BaseException):
            configEditor.remove_from_config(args)

    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_remove(self, mock_get_dist_dir):
        test_pdf_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        args = MockArgs("SQ","testFile.pdf",test_pdf_path)
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor(self.dist_dir)
        configEditor.add_to_config(args)
        configEditor.remove_from_config(args)
        assert configEditor.config["sources"] == {}
        assert not os.path.exists(f"{self.dist_dir}/PDFs/SQ")
        os.rmdir(f"{self.dist_dir}/PDFs")
    
    @patch("multiSourceWordMap.configEditor.ConfigEditor.get_dist_dir")
    def test_list(self, mock_get_dist_dir):
        args = MockArgs("SQ","testFile.pdf")
        mock_get_dist_dir.return_value = self.dist_dir
        configEditor = ConfigEditor(self.dist_dir)
        configEditor.add_to_config(args)
        configEditor.list_config()
        assert True

class MockArgs():

    def __init__(self,ticker = None , source = None, location = None):
        self.ticker = ticker
        self.source = source
        self.location = location


