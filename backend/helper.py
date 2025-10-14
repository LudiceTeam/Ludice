import json
import time
import threading
import argparse
import re


def init():
    parser = argparse.ArgumentParser(description='Code helper')
    

    parser.add_argument('-n', '--name', type=str, required=True, 
                       help='File name')
    parser.add_argument('-j', '--json_name', type=int, default=18,
                       help='Json file you want to change')
    parser.add_argument('-c', '--change', action='store_true',
                       help="Json file name to put")
    
    
    args = parser.parse_args()
    
   
    if args.verbose:
        with open(args.name,"r",encoding="utf-8") as file:
            data = file.read()
        data.replace(args.json_name,args.change)
        with open(args.name,"w",encoding = "utf-8"):
            json.dump(data,file)
        return True    
                    


