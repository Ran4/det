#!/usr/bin/env python3
from typing import Dict, List, Optional
import json
import os

from setup_logging import log

opj = os.path.join

class DescriptorConfig:
    def __init__(self, descriptors, descriptor_aliases):
        self.available_descriptors: Dict = descriptors
        self.descriptor_aliases: Dict = descriptor_aliases
        
def try_get_descriptors_filename() -> str:
    possible_paths: List[str] = [
        opj("default_descriptor_config", "descriptors.json"),
        opj(os.environ["HOME"], ".config", "det", "descriptors.json"),
        "descriptors.json",
        opj("default_descriptor_config", "descriptors.json"),
    ]
    
    for possible_path in possible_paths:
        log.debug("Looking for descriptors file in `%s`", possible_path)
        if os.path.isfile(possible_path):
            log.debug("Found descriptors file `%s`", possible_path)
            return possible_path
        
    log.error("Couldn't find descriptors file anywhere")
    raise FileNotFoundError("Could not find descriptors.json")

def try_get_descriptor_aliases_filename() -> str:
    possible_paths: List[str] = [
        opj("default_descriptor_config", "descriptor_aliases.json"),
        opj(os.environ["HOME"], ".config", "det", "descriptor_aliases.json"),
        "descriptor_aliases.json",
        opj("default_descriptor_config", "descriptor_aliases.json"),
    ]
    
    for possible_path in possible_paths:
        log.debug("Looking for descriptor aliases file in `%s`", possible_path)
        if os.path.isfile(possible_path):
            log.debug("Found descriptor aliases file `%s`", possible_path)
            return possible_path
        
    log.error("Couldn't find descriptor aliases file anywhere")
    raise FileNotFoundError("Could not find descriptor_aliases.json")
        
def descriptor_config_from_args(args) -> DescriptorConfig:
    descriptors_filename = \
        args.descriptors_file or try_get_descriptors_filename()
    with open(descriptors_filename) as f:
        data = f.read()
        descriptors = json.loads(data)
        
    aliases_filename = \
        args.descriptor_aliases_file or try_get_descriptor_aliases_filename()
    with open(aliases_filename) as f:
        data = f.read()
        descriptor_aliases = json.loads(data)
        
    return DescriptorConfig(descriptors, descriptor_aliases)
