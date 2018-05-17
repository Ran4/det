# Det - Data gET

A command-line application to output and manage generated values.

Requires Python >= 3.6.

## Use

```bash
$ det get personnummer  # Outputs a single random personnummer
19801019-2438
```

```bash
$ det get personnummer:default -n 3  # Three values, using tag "default"
20101010-1234
19831409-3434
19731409-4210
```

```bash
$ det stream personnummer  # Forever streams from the `personnummer` descriptor
20101010-1234
19831409-3434
19731409-4210
19931409-1218
...
^C
```

```bash
$ det get integer -n 4  # Forty random integers
489
472
58
268
```

```bash
$ det get integer -n 4 --source always_one --no-random
1
1
1
1
```

## Concept overview

* **Descriptor** - A string `{descriptor_name}:{descriptor_tag}`.
    When the `descriptor_tag` is missing, `default` is used instead.
    
* **Descriptor source** - Each Descriptor should have one or more descriptor sources.
    Describes how to generate values for a specific descriptor.
    Every source is named, with the default source name being `default`.
    
* **Descriptor pipeline** - Describes how to transform a value before
    output.
    Every pipeline is named, with the default pipeline name being `default`.
    
The descriptors with their sources and pipelines are defined in a file `descriptors.json`,
which should fulfill the schema found in [schemas/descriptors.js](schemas/descriptors.js).

By default, `det` will try to load descriptors from the following directories:

```
$HOME/.config/det/descriptors.json
descriptors.json
default_descriptor_config/descriptors.json
```

It can also be explicitly given with `--descriptors-file DESCRIPTORS_FILE`.

Since descriptors can be wordy at time, you can define aliases for descriptors using
`descriptor_aliases.json` file (found in the same directories as `descriptors.json`
or given using `--descriptor-aliases-file DESCRIPTOR_ALIASES_FILE`),
see [default\_descriptor\_config/descriptor\_aliases.json](default_descriptor_config/descriptor_aliases.json).

## Installing

Clone the repo. Run `./src/det.py`.
