#!/usr/bin/env python3
from typing import Dict
import json
import os

from setup_logging import log

class DescriptorConfig:
    def __init__(self, descriptors, descriptor_aliases):
        self.available_descriptors: Dict = descriptors
        self.descriptor_aliases: Dict = descriptor_aliases
        
def descriptor_config_from_args(args) -> DescriptorConfig:
    descriptors_filename = os.path.join("default_config", "descriptors.json")
    with open(descriptors_filename) as f:
        data = f.read()
        descriptors = json.loads(data)
        
    aliases_filename = os.path.join("default_config", "descriptor_aliases.json")
    with open(aliases_filename) as f:
        data = f.read()
        descriptor_aliases = json.loads(data)
        
    return DescriptorConfig(descriptors, descriptor_aliases)
