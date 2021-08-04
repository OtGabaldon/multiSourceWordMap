import os
import json
import shutil
from multiSourceWordMap.utils import is_website

class ConfigEditor:

    def __init__(self, package_path = None, dist_dir = None):
        try:
            if dist_dir:
                config_path = f"{dist_dir}/multiSourceWordMap/config.json"
                if os.path.exists(config_path):
                    with open(config_path, "r") as config_file:
                        config = json.load(config_file)
                    config["package_dir"] = '/'.join(package_path.split('/')[:-1])
                else:
                    config = {
                        "package_dir": '/'.join(package_path.split('/')[:-1]),
                        "sources": {}
                    }
                with open(config_path, "w+") as config_file:
                    config_file.write(json.dumps(config))
                self.config = config
            else:
                self.config = self.get_config()

        except FileNotFoundError:
            raise BaseException (f"Config file not found.")

    def add_to_config(self,args):
        ticker,location,source = args.ticker,args.location,args.source
        locationString = location or ""
        sources = self.config["sources"]
        if ticker not in sources:
            sources[ticker] = []
        if source in sources[ticker]:
            print(f"{source} is already in the sources list for {ticker}.")
            return

        print(f"Adding {source} {locationString} to {ticker} folder test")
        sources[ticker].append(source)
        self.config["sources"] = sources

        package_dir = self.config["package_dir"]
        if location:
            if is_website(location):
                raise BaseException("Can not specify location for website.")

            pdf_path = f"{package_dir}/PDFs/{ticker}/{source}"
            mkdir_path = pdf_path.split("/")[-1]
            dest_no_file = "/".join(mkdir_path)
            os.makedirs(dest_no_file)

            try:
                shutil.copyfile(location,pdf_path)
                print(f"Copying file \nFrom:{location} \nTo:{pdf_path}")
            except FileNotFoundError as e:
                print(f"Could not find file at :{location}. Did not add to config.")
        self.write_config(self.config)

    def remove_from_config(self, args):
        source,ticker = args.source, args.ticker
        print(f"Removing {source} from {ticker} folder")
        sources = self.config["sources"]
        if ticker in sources:
            if source in sources[ticker]:
                sources[ticker].remove(source)
                if not is_website(source):
                    pdf_path = f"{self.config['package_dir']}/PDFs/{ticker}/{source}"
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
            else:
                raise BaseException(f"{source} not in {ticker}")
        else:
            raise BaseException(f"{ticker} not in sources")
        self.write_config()

    def list_config(self):
        print("Config:")
        for ticker in self.config["sources"]:
            print(f"\n\t{ticker}:")
            for source in self.config["sources"][ticker]:
                print(f"\n\t   {source}")

    def get_config(self):
        config_editor_path = os.path.realpath(__file__)
        config_path = '/'.join(config_editor_path.split('/')[:-1]) + '/config.json'
        
        with open(config_path,'r') as config_file:
            config = json.load(config_file)

        return config

    def write_config(self, config = None):
        config_editor_path = os.path.realpath(__file__)
        config_path = '/'.join(config_editor_path.split('/')[:-1]) + '/config.json'
        with open(config_path,'w') as config_file:
            if not config:
                config_file.write(json.dumps(self.config)) 
            else:
                config_file.write(json.dumps(config))

            
