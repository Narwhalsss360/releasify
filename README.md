# Releasify

Automatically configure development repositories for release.

*See an [example scenario](#example-scenerio)*

*See [known issues](#known-issues)*

# Configuration File

*When the program runs, it will automatically look for a file matching the regex `releas(e|ify).(json|yaml|yml)`. it's best to use either releasify.json or releasify.yaml*

**Properties**
* work-in **path**: The directory to work in, defuault is directory of configuration file
* retries **int**: If an action fails, then this is how many times, it can be retried
* silenty_continue **boolean**: Whether to ignore failures and continue running actions
* actions **list**: A list of actions
* log_flle **path**: An output file that logs all actions that ran


*The other action properties depend on the function. Most function use source/src, destination/dst or path* 

**Action Properties**
* action **str**: Name of action

# Built-in Actions

* copy/cp:
    * source/src: Folder/File to copy *may be glob*
    * destination/src: Destination
* move/mv:
    * source/src: Folder/File to move *may be glob*
    * destination/src: Destination
* delete/del/remove/rm
    * path/source/src: Folder/File to delete
* script:
    * source/src: Path to python script to execute, To log from the script, set global variable `script_eval`.
* subprocess:
    * args: List of strings for shell subprocess *Name of shell command is first string*

# Example Scenerio

**Folder/Files Before**
```
.
├── LICENSE
├── README.md
├── releasify.yaml
├── docs
│   └── HELP.md
├── include
│   ├── a.h
│   └── b.h
├── releasify.yaml
├── src
│   ├── a.cpp
│   └── b.cpp
└── tests
    ├── a.test.cpp
    └── b.test.cpp
```

**Configuration**
```
actions:
  - action: move
    source: docs/HELP.md
    destination: .
  - action: rm
    path: tests
  - action: mv
    source: src/*
    destination: .
  - action: move
    source: include/*
    destination: .
  - action: delete
    path: releasify.yaml
```


**Folder/Files After**
```
.
├── HELP.md
├── LICENSE
├── README.md
├── a.cpp
├── a.h
├── b.cpp
└── b.h
```

# API

Currently, the API does no dynamic loading. For extensibility, the source package must be modified.

**Creating an action**
1. Create a function that represents an action, and the keyword arguments will be the action arguments passed from the configuration file.
2. Register the action using the `action_handler` decorator. The argument is a tuple of names. The first item in the tuple is the name, and the rest are aliases.
3. Return something from your function as a log, such as size moved, what was moved or that anything even happened.
4. Use other tools to make simpler functions.

**Other tools**
* `alias_kwargs` decorator:
    * Give aliases to keyword arguments. Pass a dictionary of strings to tuples. The string is the keyword, the tuple is the aliases.
    * Example: `@alias_kwargs({'source': ('src',), 'destination': ('dst',)})`
* `auto_glob` decorator:
    * *Only for source->destination actions* When a glob is passed in as an action property, `auto_glob` will pass into your function each glob result, given a source glob, and destination folder. Specify your source and destination parameter names, and positions.
    * Ex. `@auto_glob((0, 'source'), (1, 'destination'))`
* `auto_parse_str` decorator:
    * Automatically parse strings as another type for your functions. Specify parameter's position, name and a parse function *may be a class such as str*
    * Ex. `@auto_parse_str({(0, 'source'): Path})`

# Known issues

* glob mixed with kwarg_aliasing doesn't work
