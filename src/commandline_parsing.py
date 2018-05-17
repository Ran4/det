#!/usr/bin/env python3
import argparse

def add_reading_args_to_parser(parser) -> None:
    """Used by the GET and STREAM subparsers
    """
    parser.add_argument("descriptor", type=str)
    
    parser.add_argument("-r", "--random", action='store_true',
        help="Get random")
    
    parser.add_argument("-s", "--source-name", type=str, default="default",
        metavar="SOURCE_NAME",
        help='(default "default")')
        
    parser.add_argument("-n", type=int, default=1, 
        help="Output up to n objects")
    
def add_get_subcommand_parser(subparsers) -> None:
    get_subparser = subparsers.add_parser("get", help="Get objects")
    add_reading_args_to_parser(get_subparser)
    get_subparser.set_defaults(subcommand="get")
    
def add_stream_subcommand_parser(subparsers) -> None:
    stream_subparser = subparsers.add_parser("stream",
        help="Get objects as a stream")
    add_reading_args_to_parser(stream_subparser)
    stream_subparser.set_defaults(subcommand="stream")
    
def get_toplevel_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(
        description="Det, DatagET",
        prefix_chars='-/'  # Allow both linux and "windows-style" prefixes
    )
    
    subparsers = arg_parser.add_subparsers()
    add_get_subcommand_parser(subparsers)
    add_stream_subcommand_parser(subparsers)
    
    return arg_parser