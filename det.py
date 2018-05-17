#!/usr/bin/env python3
from typing import List, Any, Optional
import argparse
import itertools
import random
import sys


class Descriptor:
    def __init__(self, name: str, tag: Optional[str]=None):
        self.name = name
        self.tag = tag

    @staticmethod
    def from_string(s: str) -> Optional["Descriptor"]:
        if s == "personnummer":
            descriptor =  Descriptor(name="personnummer", tag=None)
        else:
            descriptor = None
            
        if descriptor is not None:
            v("Found descriptor {descriptor}")
        else:
            v("Found descriptor {descriptor}")
            
        return descriptor

def get_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(
        description="Det, DatagET",
        prefix_chars='-/'  # Allow both linux and "windows-style" prefixes
    )
        
    arg_parser.add_argument("term", type=str)
    
    #~ arg_parser.add_argument("-s", "--sort", metavar="TERM",
    #~     help="sort in ascending order according to TERM")
        
    #~ arg_parser.add_argument("-d", "--sortd", metavar="TERM",
    #~     help="sort in descending order")
        
    #~ arg_parser.add_argument("-r", "--re", action='store_true',
    #~     help="search using regular expressions")
        
    #~ arg_parser.add_argument("-o", "--out", dest="outfile",
    #~         default="outfile.txt")
    
    arg_parser.add_argument("-r", "--random", action='store_true',
        help="get random")
        
    arg_parser.add_argument("-n", type=int, default=1,
            help="returns max n results")
        
    #~ arg_parser.add_argument("-m", "--min", nargs=2, metavar=("TERM", "VALUE"),
    #~     help="requires TERM to be equal to or more than VALUE")
        
    #~ arg_parser.add_argument("-M", "--max", nargs=2, metavar=("TERM", "VALUE"),
    #~     help="requires TERM to be equal to or less than VALUE")
    
    return arg_parser

def get_personnummers():
    personnummers = [
        "19801019-2438",
        "19831409-3434",
        "20101010-1234",
        "19192349-4488",
    ]
    
    return personnummers

def get_values(args) -> List[Any]:
    if args.term == "personnummer":
        values = get_personnummers()
        return values
    else:
        print("Unrecognized term {args.term}")
        exit(1)
    
def det(args):
    print(f"# args: {args}")
    
    descriptor = Descriptor.from_string(args.term)
    
    values = get_values(args)
        
    if args.random:
        values = random.sample(values, min(len(values), args.n))
        
    for x in itertools.islice(values, args.n):
        print(x)

def main():
    parser = get_parser()
    
    if len(sys.argv) > 1:
        args = parser.parse_args()
        det(args)
    else:
        args = parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()
