#from configEditor import ConfigEditor
from multiSourceWordMap.configEditor import ConfigEditor
from multiSourceWordMap.getArgs import get_args

def main():
    args = get_args().parse_args()
    if(args.sub_command == "config"):
        configEditor = ConfigEditor()
        if(args.config_sub_command == "add"):
            configEditor.add_to_config(args)
        elif(args.config_sub_command == "remove"):
            configEditor.remove_from_config(args)
        elif(args.config_sub_command == "list"):
            configEditor.list_config(args)
    elif(args.sub_command == "make"):
        if(args.source):
            print(f"Making wordmap from {args.source}")
        else:
            print(f"Making wordmap for {args.ticker}")
    

if __name__ == "__main__":
    main()