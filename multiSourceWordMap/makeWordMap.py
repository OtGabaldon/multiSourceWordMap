from wordcloud import WordCloud
from extraction.extractor import Extractor
import sys

def getArgs():
    args = sys.argv
    return (
        args[1] #info_location
    )

def makeWordMap():
    info_location = getArgs()
    extractor = Extractor(info_location)
    file_path = extractor.create_text_file()
    with open(file_path,"r") as readFile:
        text = readFile.read()
    wordcloud = WordCloud().generate(text)
    wordcloudImage = wordcloud.to_image()
    wordcloudImage.save('../wordClouds/SQ/wordCloud.png')

makeWordMap()
