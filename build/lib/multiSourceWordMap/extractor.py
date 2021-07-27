import PyPDF2
import os

class Extractor:

    def __init__(self,info_location):
        self.info_location = info_location
        self.is_website = "www." in info_location
        self.pdf_location = self.build_pdf_location()

    def create_text_file(self):
        if(self.is_website):
            print("Extracting from website")
            self.extract_from_website_to_text()
        else:
            print(f"Extracting from pdf {self.info_location}")
            self.extract_from_pdf_to_text()

            
    def extract_from_pdf_to_text(self):
        pdfFile = open(self.pdf_location,"rb")
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        numPages = pdfReader.getNumPages()
        text = ""
        for pageNum in range(numPages):
            page = pdfReader.getPage(pageNum)
            text += page.extractText()
        
        outPath,exists = self.create_text_file_path()
        textOutFile = open(outPath,"w")
        textOutFile.write(text)

    def extract_from_website_to_text():
        print("Not yet implemented")

    def create_text_file_path(self):
        new_path = self.build_text_file_path()
        text_files_location,stock_ticker,text_file_name = new_path.split('/')

        if(not os.path.exists(text_files_location)):
            os.mkdir(text_files_location)
        if(not os.path.exists(rf"{text_files_location}/{stock_ticker}")):
            os.mkdir(rf"{text_files_location}/{stock_ticker}")
        if(os.path.exists(newPath)):
            os.remove(newPath) # always renew file

    def build_text_file_path(self):
        text_files_location = r"../../textFiles"
        stock_ticker,source_location = self.info_location.split('/')
        text_file_name = source_location.split(".")[0] + ".txt"
        return fr"{text_files_location}/{stock_ticker}/{text_file_name}"

    def build_pdf_location(self):
        return rf"../PDFs/{self.info_location}"


