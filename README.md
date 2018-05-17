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

## Concept overview

* **Descriptor** - A string `{descriptor_name}:{descriptor_tag}`.
    When the `descriptor_tag` is ommitted, `default` is used instead.
    
* **Descriptor source** - Each Descriptor should have one or more descriptor sources.
    Describes how to generate values for a specific descriptor.
    Every source is named, with the default source name `default`.

## Installing

Clone the repo. Run `./src/det.py`.
