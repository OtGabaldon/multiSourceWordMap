from multiSourceWordMaps.utils import *
import unittest
import os

class TestUtils(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
       return


    def test_is_website(self):
        assert is_website('https://google.com')
        assert is_website('www.google.com')
        assert is_website('www.google.com/test/site/path')
        assert not is_website('test.pdf')
        assert not is_website('path/to/test.pdf')
    
    def test_get_source_name(self):
        website_source_name = get_source_name("www.google.com/path/to/test")
        assert website_source_name == "www.google.compathtotest"
        pdf_source_name = get_source_name("path/to/pdfTest.pdf")
        assert pdf_source_name == "pdfTest"

    def test_create_pdf_file_path(self):
        pdf_file_path = create_pdf_file_path(f"{os.path.dirname(os.path.abspath(__file__))}","TSLA","tsla.txt")
        assert pdf_file_path == f"{os.path.dirname(os.path.abspath(__file__))}/PDFs/TSLA/tsla.pdf"
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/PDFs/TSLA")
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/PDFs")
    
    def test_create_png_file_path(self):
        pdf_file_path = create_png_file_path(f"{os.path.dirname(os.path.abspath(__file__))}","TSLA","tsla.txt")
        assert pdf_file_path == f"{os.path.dirname(os.path.abspath(__file__))}/maps/TSLA/tsla.png"
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/maps/TSLA")
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/maps")
    
    def test_create_text_file_path(self):
        pdf_file_path = create_text_file_path(f"{os.path.dirname(os.path.abspath(__file__))}","TSLA","tsla.txt")
        assert pdf_file_path == f"{os.path.dirname(os.path.abspath(__file__))}/text/TSLA/tsla.txt"
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/text/TSLA")
        os.rmdir(f"{os.path.dirname(os.path.abspath(__file__))}/text")