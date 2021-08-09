from multiSourceWordMap.extractor import Extractor
from unittest.mock import patch
import os
import unittest
from mock_args import MockArgs
from mock_requests import MockData
from mock_config_editor import MockConfigEditor

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text_data, status_code):
            self.text = text_data
            self.status_code = status_code

    test_website_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_website/{args[0]}"
    with open(test_website_path,'r') as website_file:
        data = website_file.read()
    
    return MockResponse(data, 200)

class TestExtractor(unittest.TestCase):
    
    @patch("multiSourceWordMap.extractor.create_text_file_path")
    @patch("multiSourceWordMap.extractor.create_pdf_file_path")
    @patch("multiSourceWordMap.extractor.ConfigEditor")
    def test_pulling_text_from_pdf(self, mock_config_editor, mock_create_pdf_file_path, mock_create_text_file_path):
        mock_config_editor.return_value = MockConfigEditor(
            {
                "package_dir":"test/path",
                "sources":[]
            }
        )
        mock_create_pdf_file_path.return_value = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_pdfs/testPdf.pdf"
        mock_create_text_file_path.return_value = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_text/testPdf.txt"
        extractor = Extractor(MockArgs(
            ticker="SQ",
            source="testFile.pdf"
        ))

        extractor.pull_text_from_source()
        test_text_file = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_text/testPdf.txt"
        with open(test_text_file,"r") as textFile:
            test_text = textFile.read()
        assert test_text == "This is a test pdf with  character With periods and  weird chars"
        os.remove(test_text_file)

    @patch("multiSourceWordMap.extractor.create_text_file_path")
    @patch("multiSourceWordMap.extractor.requests.get", side_effect=mocked_requests_get)
    @patch("multiSourceWordMap.extractor.ConfigEditor")
    def test_pulling_text_from_website(self, mock_config_editor, mock_requests_get, mock_create_text_file_path):
        test_site_text = """<body>
    <h1>This is a header</h1>
    <p>This is text</p>
    <div>
        <section>
            <p>This is a nested section</p>
            <p>This is a second nested section</p>
        </section>
    </div>
    <img src="Notrealimage.jpg">
    <table>
        <th>header</th>
        <td>
            <tr>
                row 1
            </tr>
        </td>
    </table>
</body>"""
        mock_config_editor.return_value = MockConfigEditor(
            {
                "package_dir":"test/path",
                "sources":[]
            }
        )
        text_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_text/testSite.txt"
        mock_create_text_file_path.return_value = text_file_path
        test_website_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_website/www.testSite.html"
        extractor = Extractor(MockArgs(
            ticker="SQ",
            source="www.testSite.html"
        ))
        extractor.pull_text_from_source()
        with open(test_website_path,'r') as website_file:
            assert test_site_text == website_file.read()  
        os.remove(text_file_path)

