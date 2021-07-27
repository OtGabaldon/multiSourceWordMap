import os
import json


class ConfigEditor:

    def __init__(self):
        try:
            with open('./config.json','r') as config_file:
                config = json.load(config_file)
            with open('./config.json','w') as config_file:
                path_parent = os.path.dirname(os.getcwd())
                os.chdir(path_parent)
                config['base_dir'] = os.getcwd()
                self.config = config
                json.dump(config, config_file)
        except FileNotFoundError:
            print(f"Config file not found at {os.getcwd()}/config.json")
