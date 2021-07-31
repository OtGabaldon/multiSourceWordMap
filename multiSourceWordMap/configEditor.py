import os
import json
import shutil


class ConfigEditor:

    def __init__(self, setup_dir = None):
        try:
            self.config = self.get_config()
            if setup_dir:
                setup_dir_array = setup_dir.split('/')
                setup_dir_array.pop() #remove setup.py file
                base_dir = '/'.join(setup_dir_array)
                self.config['base_dir'] = base_dir 
            if "sources" not in self.config:
                self.config["sources"] = {}
            self.write_config()
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

        base_dir = self.config["base_dir"]
        if location:
            if self.is_website(location):
                raise BaseException("Can not specify location for website.")
                return

            pdf_path = f"{base_dir}/PDFs/{ticker}/{source}"
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
                if not self.is_website(source):
                    pdf_path = f"{self.config['base_dir']}/PDFs/{ticker}/{source}"
                    os.remove(pdf_path)
            else:
                raise BaseException(f"{source} not in {ticker}")
        else:
            raise BaseException(f"{ticker} not in sources")
        self.write_config()

    def list_config(self,args):
        print("Config:")
        for ticker in self.config["sources"]:
            print(f"\n\t{ticker}:")
            for source in self.config["sources"][ticker]:
                print(f"\n\t   {source}")

    def get_config(self):
        print(os.path.realpath(__file__))
        print(os.getcwd())
        
        with open('./config.json','r') as config_file:
            config = json.load(config_file)

        return config

    def write_config(self, config = None):
        with open('./config.json','w+') as config_file:
            if not config:
                config_file.write(json.dumps(self.config)) 
            else:
                config_file.write(json.dumps(config))

    def is_website(self,location):
        return len(location.split("www.")) > 1
            
