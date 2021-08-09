
class MockRequests:

    def __init__(self):
        return

    def get(self, source):
        test_website_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_data/test_website/{source}"
        with open(test_website_path,'r') as website_file:
            return MockData(website_file.read())
        

class MockData:
    def __init__(self,text):
        self.text = text
