from wordcloud import WordCloud
from multiSourceWordMap.configEditor import ConfigEditor
from multiSourceWordMap.utils import create_png_file_path, create_text_file_path

class MapCreator:

    def __init__(self,args):
        self.config = ConfigEditor().config["package_dir"]
        self.ticker = args.ticker
        self.source = args.source

    def make_map_from_text(self):
        text_path = create_text_file_path(
            self.config,
            self.ticker,
            self.source
        )
        png_path = create_png_file_path(
            self.config,
            self.ticker,
            self.source
        )
        print(text_path)
        print(png_path)
        self.makeWordMap(text_path, png_path)
        return

    def makeWordMap(self, text_path, png_path):
        with open(text_path,"r") as readFile:
            text = readFile.read()
        wordcloud = WordCloud().generate(text)
        wordcloudImage = wordcloud.to_image()
        wordcloudImage.save(png_path)
