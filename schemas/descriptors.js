/* @flow */
/* Schema defined in Facebook Flow */

type FileSource = {
    "file": string,
}

type CommandSource = {
    "cmd": string,
}

type DescriptorsFile = {
    [descriptorName: string]: {
        sources?: {
            [sourceName: string]:
                | {
                  "file": string,
                } | {
                  "cmd": string
                },
        },
        pipelines?: {
            [pipelineName: string]: {
                "template": string,
            }
        }
    }
}

let exampleDescriptorsFile: DescriptorsFile = {
    "swedish_personnummer:default": {
            "sources": {
                "default": {
                    "file": "example_data/swedishpersonnummers.txt"
                },
                "another": {
                    "cmd": "echo 42"
                }
            },
            "pipelines": {
                "sql": {
                    "template": "INSERT INTO {dbname} VALUES {0}"
                }
            }
      }
}
