/* @flow */
/* Schema defined in Facebook Flow */

type FileSource = {
    "file": string,
}

type DescriptorsFile = {
    [descriptorName: string]: {
        sources?: {
            [sourceName: string]:
                | FileSource,
        },
        pipelines?: {
            [pipelineName: string]: {
                "template": string,
            }
        }
    }
}

let exampleDescriptorsFile: DescriptorsFile = {
    "personnummer:default": {
            "sources": {
                "default": {
                    "file": "example_data/swedishpersonnummers.txt"
                }
            },
            "pipelines": {
                "sql": {
                    "template": "INSERT INTO {dbname} VALUES {0}"
                }
            }
      }
}
