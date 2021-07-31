#from configEditor import ConfigEditor
from multiSourceWordMap.configEditor import ConfigEditor
from multiSourceWordMap.getArgs import get_args

def main():
    args = get_args().parse_args()
    if(args.sub_command == "config"):
        configEditor = ConfigEditor()
        print(configEditor.config)
        if(args.config_sub_command == "add"):
            configEditor.add_to_config(args)
        elif(args.config_sub_command == "remove"):
            print(f"Removing {args.source} from {args.ticker} folder")
        elif(args.config_sub_command == "list"):
            print("Listing config")
    elif(args.sub_command == "make"):
        if(args.source):
            print(f"Making wordmap from {args.source}")
        else:
            print(f"Making wordmap for {args.ticker}")
    

if __name__ == "__main__":
    main()