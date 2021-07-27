#from configEditor import ConfigEditor
from multiSourceWordMap.getArgs import get_args

def main():
    args = get_args().parse_args()
    if(args.sub_command == "config"):
        if(args.config_sub_command == "add"):
            print(f"Adding {args.source} {args.location} to {args.ticker} folder")
        elif(args.config_sub_command == "remove"):
            print(f"Removing {args.source} from {args.ticker} folder")
        elif(args.config_sub_command == "list"):
            print("Listing config")
    elif(args.sub_command == "make"):
        if(args.source):
            print(f"Making wordmap from {args.source}")
        else:
            print(f"Making wordmap for {args.ticker}")

    #config_editor = ConfigEditor()
    #if()
    # edit config
    
    #extract from config and make map
        #extractor = Extractor()
        #word_map_generator = WordMapGenerator()
    

if __name__ == "__main__":
    main()