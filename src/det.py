#!/usr/bin/env python3
from typing import List, Dict, Any, Optional
import itertools
import random
import sys

from commandline_parsing import get_toplevel_parser
from descriptor_config import descriptor_config_from_args
from descriptor import Descriptor, descriptor_from_raw_string
from setup_logging import log

def det(args):
    config = descriptor_config_from_args(args)
    
    descriptor: Descriptor = \
        descriptor_from_raw_string(config, args.descriptor)
    
    if args.subcommand in ["get", "stream"]:
        values = descriptor.get_values(args)
        if args.random:
            # Consume the entire list of values
            values = list(values)
    
    if args.subcommand == "get":
        if args.random:
            values = random.sample(values, min(len(values), args.n))
            
        for x in itertools.islice(values, args.n):
            print(x)
            
    elif args.subcommand == "stream":
        if args.random:
            # Consume the entire list of values, then pick randomly from there
            all_values = list(descriptor.get_values(args))
            while True:
                print(random.choice(all_values))
        else:
            while True:
                values = descriptor.get_values(args)
                for value in values:
                    print(value)
                    
    else:
        raise Exception(f"Unrecognized subcommand {args.subcommand}")

def main():
    parser = get_toplevel_parser()
    
    if len(sys.argv) > 1:
        parsed_args = parser.parse_args()
        
        # Make sure --no-random overrides --random:
        # TODO: Figure out a way to do this with argparse's config 
        if parsed_args.no_random:
            parsed_args.random = False
            
        log.info("args: %s", parsed_args)
            
        det(parsed_args)
    else:
        args = parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()
