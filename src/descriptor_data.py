#!/usr/bin/env python3
import os

available_descriptors = {
    "personnummer:default": {
        "sources": {
            "default": {
                "file": "example_data/swedishpersonnummers.txt",
            },
        },
        "pipelines": {
            "sql": {
                "template": "INSERT INTO {dbname} VALUES {0}",
            },
        },
    }
}

#TODO: Read from file
descriptor_aliases = {
    "pn": "personnummer",
}