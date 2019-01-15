# JSON Inspector

An expiramental tool to compare and flatten json-formatted logs for
SIEM ingestion.

## Prerequisites

- Install Python 3.6+

## Installation

Create your virtual environment and install dependencies.

```bash
$ git clone thisrepo.git
$ cd thisrepo
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Modeling logs

Json-inspect models logs by parsing JSON objects and then converting
them to __minion__ objects. As a minion,
Json-inspect stores the data of the log values as well as a _model_ of
the data.

The model is helpful because we can use it to compare log structures
of logs with varying content. We can also output the data by using
the same minion if needed.

The following JSON data types do not change the structure of the log.
The model will label these datatypes as __edge__ so that when we
compare the models, the labels will be equivalent:
- Integer
- String
- Bool
- Null

The following data types do change the structure of the log so their
labels are set as 'DICT' and 'LIST' respectively:
- object/dictionary/hash table
- array/list

If you converted ```[123, "my_string"]``` to a string and then hashed
it, the hash would be different than the hash for ```[456, "AnotherString"]```.
Using the labels from our log models, however, these two lists would be
converted to ```["edge", "edge"]``` and would result in an equivalent
hash for both logs. This is essentially how we compare logs that
contain varying data.

To take it a step further, json-inspect models the above as ```["edges_only"]```
so that the hash stays the same whether you have two edges or forty-five.
It acts this way because having forty-five edges does not change the
_structure_ of the log, only the quantity of items in the list.

To model log data, json-inspect ingests each data value in a log into
an object called a __minion__. A minion contains the following items
(but not limited to storing just these items):
- Data value it represents
- The label of the data type (edge, DICT, LIST, etc.)
- Child minions, like in the case of a dictionary or list.

An example log:

```javascript
{
  "key1": "value1",
  "key2": {
    "key3": 123
  },
  "key4": ["Hello"]
}
```
To simplify, you can think of this JSON object being stored like this:

```javascript
DictMinion(
  label="DICT",
  data={
  "key1": EdgeMinion(label="edge", data="value1"),
  "key2": DictMinion(
    label="DICT"
    data={"key3": EdgeMinion(label="edge", data=123)}
  )
  "key4": ListMinion(
    label="LIST",
    data=[EdgeMinion(label="edge", data="Hello")]
  )
}
```
 
## Quickstart

To run the program, you create a __master__. The master api give you
access to various functions to ingest logs and output the unique log
structures and models.

- Master.**print_unique_models**(resolution=0, indent=None)
  - Prints the __model__ for the log based on resolution (how deep you want to
  represent the log). You can pretty print by using indent.
- Master.**print_unique_data**(resolution=0, indent=None)
  - Prints the __data__ for the log based on resolution specified.
- Master.**write_unique_models**(output_file, resolution=0, indent=None)
  - Writes the models to file.
- Master.**write_unique_data**(output_file, resolution=0, indent=None)
  - Writes the data to file.
- Master.**write_unique_data_recursive**(output_file, resolution=0, indent=None)
  - Recursively starts at the resolution defined, notes unique log models,
  then subtracts 1 from the resoltuion and repeats until resolution == 0-.
  This gives you a thorough run through high-volume logs.

```python
from json_inspect import master

m = master.Master(input_file="readme.json")
m.make()

# These commands will step through the structure of the log model.
# These functions will help to identify where your logs can be
# flattened.
m.print_unique_models(resolution=0, indent=2)
m.print_unique_models(resolution=1, indent=2)
m.print_unique_models(resolution=2, indent=2)
m.print_unique_models(resolution=3, indent=2)

# These commands will display actual data from the logs that represent
# the log structure. This command is helpful when you're actually
# writing your filters in Logstash or transforms in Splunk.
m.print_unique_data(resolution=0, indent=2)
m.print_unique_data(resolution=1, indent=2)
m.print_unique_data(resolution=2, indent=2)
m.print_unique_data(resolution=3, indent=2)

```

The output looks like this:


```bash

# m.print_unique_models(resolution=0, indent=2)

# Both example logs share the same structure / hash at this
# resolution.
{
  "7346da258c47dc6dcf2cf6184638c91f": {
    "key1": "edge",
    "key2": "edge",
    "key3": "LIST",
    "key4": "DICT"
  }
}

# m.print_unique_models(resolution=1, indent=2)

# Log structure begins to differ at this resolution.
{
  "1a8a5c002dfec9aa58e65af353c969e4": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "DICT(s)",
      "LIST(s)",
      "edge(s)"
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  },
  "14d538d29f4ea8d6ba2556a689bcd357": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "LIST(s)",
      "edge(s)"
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  }
}

# m.print_unique_models(resolution=2, indent=2)
{
  "781e58e33dde2b7de3c5e01f81bfd611": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "edge",
      "edge",
      "DICT_KEYS: ['NestedKey1']",
      "edge",
      "edge",
      [
        "edges_only"
      ]
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  },
  "8eb0c3f7ceaa8359ec3b22c642929769": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "edge",
      "edge",
      "edge",
      "edge",
      "edge",
      [
        "edges_only"
      ]
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  }
}

# m.print_unique_models(resolution=3, indent=2)
 {
  "781e58e33dde2b7de3c5e01f81bfd611": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "edge",
      "edge",
      "DICT_KEYS: ['NestedKey1']",
      "edge",
      "edge",
      [
        "edges_only"
      ]
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  },
  "8eb0c3f7ceaa8359ec3b22c642929769": {
    "key1": "edge",
    "key2": "edge",
    "key3": [
      "edge",
      "edge",
      "edge",
      "edge",
      "edge",
      [
        "edges_only"
      ]
    ],
    "key4": "DICT_KEYS: ['NestedKey2']"
  }
}

# Now for the data functions:

# m.print_unique_data(resolution=0, indent=2)

# Note that while both logs would result in the same hash based on the
# models, we only display data from one of them as they both share
# the same structure. This is helpful when writing transforms and
# filters based on actual data from a unique model structure.
{
  "7346da258c47dc6dcf2cf6184638c91f": {
    "key1": "MyString",
    "key2": 12345,
    "key3": "LIST",
    "key4": "DICT"
  }
}
# m.print_unique_data(resolution=1, indent=2)

# Note that as the models/structure of the logs start to differ, we
# output data for each unique model.
{
  "1a8a5c002dfec9aa58e65af353c969e4": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "DICT(s)",
      "LIST(s)",
      "edge(s)"
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  },
  "14d538d29f4ea8d6ba2556a689bcd357": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "LIST(s)",
      "edge(s)"
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  }
}

# m.print_unique_data(resolution=2, indent=2)
{
  "781e58e33dde2b7de3c5e01f81bfd611": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "ListItem",
      54321,
      {
        "NestedKey1": "NestedValue"
      },
      true,
      null,
      [
        "edge(s)"
      ]
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  },
  "8eb0c3f7ceaa8359ec3b22c642929769": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "ListItem",
      54321,
      "NotNestedValue",
      false,
      null,
      [
        "edge(s)"
      ]
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  }
}

# m.print_unique_data(resolution=3, indent=2)
{
  "781e58e33dde2b7de3c5e01f81bfd611": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "ListItem",
      54321,
      {
        "NestedKey1": "NestedValue"
      },
      true,
      null,
      [
        "InnerList",
        "MoreInnerList"
      ]
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  },
  "8eb0c3f7ceaa8359ec3b22c642929769": {
    "key1": "MyString",
    "key2": 12345,
    "key3": [
      "ListItem",
      54321,
      "NotNestedValue",
      false,
      null,
      [
        "InnerList",
        "MoreInnerList"
      ]
    ],
    "key4": {
      "NestedKey2": "SomeValue"
    }
  }
}

```
Using the Python REPL, here's another example parsin through logs from
a high-volume data source.

![Large volume example image](REPL-Large-Volume.png "Large volume example")

The output in the Python REPL would lo