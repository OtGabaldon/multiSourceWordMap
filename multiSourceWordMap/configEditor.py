import os
import json


class ConfigEditor:

    def __init__(self):
        try:
            self.config = self.get_config()
            self.config['base_dir'] = os.getcwd()
            if "sources" not in self.config:
                self.config["sources"] = {}
            self.write_config(self.config)
        except FileNotFoundError:
            print(f"Config file not found at {os.getcwd()}/config.json")

    def get_config(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)

        return config

    def write_config(self, config):
        with open('./config.json','w+') as config_file:
             config_file.write(json.dumps(config))

        print(json.dumps(self.get_config()))

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
        self.write_config(self.config)
