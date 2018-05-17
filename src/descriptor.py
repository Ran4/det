from typing import List, Dict, Any, Optional
from abc import ABC
import subprocess
import shlex

from descriptor_config import DescriptorConfig
from helpers import map_dict
from setup_logging import log

class DescriptorSource(ABC):
    def __init__(self):
        raise Exception("DescriptorSource is an abstract baseclass")
    
    def get_values(self):
        raise Exception("DescriptorSource is an abstract baseclass")
    
class DescriptorSourceFile(DescriptorSource):
    def __init__(self, filename: str):
        self.filename = filename
        
    def get_values(self):
        with open(self.filename) as f:
            for line in f:
                line_without_trailing_newline = line[:-1]
                yield line_without_trailing_newline
                
class DescriptorSourceCommand(DescriptorSource):
    def __init__(self, command: List[str]):
        if isinstance(command, str):
            raise Exception("Command must be given as list of str")
        self.command = command

    def get_values(self):
        popen = subprocess.Popen(self.command,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            stdout_line_without_newline = stdout_line[:-1]
            yield stdout_line_without_newline
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, self.command)
        
class DescriptorPipeline(ABC):
    def __init__(self):
        raise Exception("DescriptorSource is an abstract baseclass")
    
    
class DescriptorTemplatePipeline(DescriptorPipeline):
    def __init__(self, template):
        self.template = template

    def apply(self):
        # TODO: Implement this
        pass
    
def descriptor_source_from_dict(d: Dict) -> DescriptorSource:
    """d is e.g. `{ "file": "example_data/swedishpersonnummers.txt"}`
    """
    if "file" in d:
        return DescriptorSourceFile(filename=d["file"])
    elif "cmd" in d:
        return DescriptorSourceCommand(command=shlex.split(d["cmd"]))
    else:
        raise RuntimeError(f"Couldn't create DescriptorSource from {d}")
    
def get_descriptor_sources_dict(config, descriptor_dict: Dict) -> \
        Dict[str, DescriptorSource]:
    descriptor_sources_dict = descriptor_dict.get("sources", {})
    return map_dict(descriptor_source_from_dict, descriptor_sources_dict)

def pipeline_from_dict(d: Dict) -> DescriptorPipeline:
    if "template" in d:
        return DescriptorTemplatePipeline(template=d["template"])
    else:
        raise RuntimeError(f"Couldn't create DescriptorPipeLine from {d}")

def get_pipelines(config, descriptor_dict: Dict) -> \
        Dict[str, DescriptorPipeline]:
    descriptor_pipelines_dict = descriptor_dict.get("pipelines", {})
    return map_dict(pipeline_from_dict, descriptor_pipelines_dict)

class Descriptor:
    def __init__(self,
            name: str,
            tag: Optional[str]=None,
            sources: Optional[Dict[str, DescriptorSource]]=None,
            pipelines: Optional[Dict[str, DescriptorPipeline]]=None,
            ):
        self.name = name
        self.tag = tag
        self.sources: Dict[str, DescriptorSource] = \
            sources if sources is not None else {}
        self.pipelines: Dict[str, DescriptionPipeline] = \
            pipelines if pipelines is not None else {}

    def __str__(self):
        return f"{self.name}:{self.tag}"
    
    def get_values(self, args):
        descriptor_source = try_find_descriptor_source(self, args)
        return descriptor_source.get_values()
    
def try_find_descriptor_source(descriptor: Descriptor, args) \
        -> DescriptorSource:
    source_name: str = args.source
    try:
        return descriptor.sources[source_name]
    except KeyError as e:
        raise KeyError(
            f"Couldn't find source named `{source_name}` "
            f"from descriptor `{descriptor}`.\nAvailable sources: "
            + ", ".join(descriptor.sources.keys())) from e
        
def split_descriptor_string(raw_descriptor_string) -> (str, str):
    """Converts e.g. "hello" or "hello:default" into ("hello", "default")"""
    if ":" in raw_descriptor_string:  # e.g. "hello" -> ("hello", "world")
        guess_name, guess_tag = raw_descriptor_string.split(":")
        return guess_name, guess_tag
    else:  # e.g. "hello:world" -> ("hello", "world")
        return raw_descriptor_string, "default"
    
def try_alias_lookup(config, alias: str) -> (str, str):
    try:
        new_raw_descriptor_string = config.descriptor_aliases[alias]
    except KeyError as e:
        msg = f"Found no descriptor or alias matching {alias}"
        log.debug(msg)
        raise Exception(msg) from e
    
    guess_name, guess_tag = \
        split_descriptor_string(new_raw_descriptor_string)
    log.debug("Found descriptor_name alias "
              f"`{alias}` -> `{guess_name}:{guess_tag}`")
    return guess_name, guess_tag
        
def try_find_existing_descriptor_name_and_tag(
        config: DescriptorConfig,
        raw_descriptor_string: str,
        look_for_alias_on_missing: bool=True) -> (str, str):
    """Returns a tuple of descriptor_name, descriptor_tag or raises"""
    guess_name, guess_tag = split_descriptor_string(raw_descriptor_string)
    log.debug(f"Looking for descriptor `{guess_name}:{guess_tag}`")
        
    if f"{guess_name}:{guess_tag}" in config.available_descriptors.keys():
        log.debug(f"Using descriptor `{guess_name}:{guess_tag}`")
        return guess_name, guess_tag
    
    if look_for_alias_on_missing:
        log.debug(
            f"Could not find `{guess_name}:{guess_tag}`. Looking for aliases")
        guess_name, guess_tag = try_alias_lookup(config, alias=guess_name)
        return try_find_existing_descriptor_name_and_tag(
            config, f"{guess_name}:{guess_tag}",
            look_for_alias_on_missing=False)
    else:
        raise KeyError(f"Could not find descriptor `{guess_name}:{guess_tag}`")

def descriptor_from_descriptor_name_and_tag(descriptor_name, descriptor_tag) \
        -> Optional[Descriptor]:
    return 

def descriptor_from_raw_string(
        config, raw_descriptor_string: str) -> Optional[Descriptor]:
    descriptor_name, descriptor_tag = \
        try_find_existing_descriptor_name_and_tag(config, raw_descriptor_string)
        
    descriptor_dict = \
        config.available_descriptors[f"{descriptor_name}:{descriptor_tag}"]
        
    descriptor_sources = get_descriptor_sources_dict(config, descriptor_dict)
    descriptor_pipelines = get_pipelines(config, descriptor_dict)
    
    if not descriptor_sources:
        print("WARNING: Found no sources for "
              f"`{descriptor_name}:{descriptor_tag}`")
    
    if not descriptor_pipelines:
        print("NOTE: Found no pipelines for "
              f"`{descriptor_name}:{descriptor_tag}`")
        
    
    descriptor = Descriptor(name=descriptor_name,
                            tag=descriptor_tag,
                            sources=descriptor_sources,
                            pipelines=descriptor_pipelines)
    return descriptor
