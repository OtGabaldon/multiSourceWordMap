import PyPDF2
import requests
from bs4 import BeautifulSoup
from multiSourceWordMap.configEditor import ConfigEditor
from multiSourceWordMap.utils import create_text_file_path, is_website

class Extractor:

    def __init__(self, args):
        self.config = ConfigEditor().config["package_dir"]
        self.source = args.source # path for pdf, url for website
        self.ticker = args.ticker
        return

    def pull_text_from_source(self):
        if is_website(self.source):
            print("Is Website")
            self.extract_from_website_to_text()
        else:
            print("Is pdf")
            self.extract_from_pdf_to_text()           

    def pull_text_for_ticker(self):
        print("Not yet implemented")
            
    def extract_from_pdf_to_text(self):
        pdfFile = open(self.source,"rb")
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        numPages = pdfReader.getNumPages()
        text = ""
        for pageNum in range(numPages):
            page = pdfReader.getPage(pageNum)
            text += page.extractText()
        outPath = create_text_file_path(
                self.config,
                self.ticker,
                self.source
            )
        textOutFile = open(outPath,"w+")
        textOutFile.write(text)
        pdfFile.close()
        textOutFile.close()

    def extract_from_website_to_text(self):
        doc = requests.get(self.source).text
        outPath = create_text_file_path(
            self.config,
            self.ticker,
            self.source
        )
        textOutFile = open(outPath,"w+")
        textOutFile.write(doc)
        textOutFile.close()



