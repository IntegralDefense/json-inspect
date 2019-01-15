# JSON Inspector

Tool to compare and flatten json-formatted logs for SIEM ingestion.

## Prerequisites

- Install Python 3.6+

## Installation

Create your virtual environment and install dependencies.

```bash
$ git clone thisrepo.git
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Modeling logs

Json-inspect models logs by parsing JSON objects and then converting
them to a 'minion' object (json_inspect/minion.py). As a minion,
Json-inspect stores the data of the log values as well as a 'model' of
the data.

The model is helpful because we can use it to compare log structures
despite the content of the log. For example, the following JSON data
types do not change the structure of the log. The model will label
these datatypes as __edges__ so that when we compare the models, the
labels will be equivalent:
- Integer
- String
- Bool
- Null

The following data types do change the structure of the log so their
labels are set as 'DICT' and 'LIST' respectively:
- object/dictionary/hash table
- array/list

If you converted ```[123, "my_string"]``` to a string and then hashed
it, the hash would be different than ```[456, "AnotherString"]```.
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
  "key1": EdgeMinion(
    label="edge",
    data="value1"
  ),
  "key2": DictMinion(
    label="DICT"
    data={"key3": EdgeMinion(label="edge", data=123)}
  )
  "key4": ListMinion(
    label="LIST",
    data=[
      EdgeMinion(label="edge", data="Hello")
    ]
  )
}
```
As you can see, we give each data point a label yet keep the data. Both
of these values can be accessed but we can use the labels to 
## Quickstart

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


#

## Overview

Many log sources utilized by security teams today are verbose and
utilize json formatting. This formatting usually has multiple tiers of
nested data within the json object.

SIEMs are not particularly great at effeciently parsing this nested
json data. To help with this, you can create filters and indexing
routines that flatten the logs. A simple log example:

```javascript
{
    "name": "John Doe",
    "device": "iPhone X",
    "location": {
        "country": "Nigeria",
        "ip_address": "10.x.x.x",
        "state": "unknown",
    }
}
```

In this example, the location values can be flattened because the keys
are not dynamic. This will help the SIEM with indexing and the data
should be easier to search. If we were using logstash, you can flatten
this log by setting up filters that transform the key-value pairs of
the location object like this:

```javascript
{
    "name": "John Doe",
    "device": "iPhone X",
    "location-country": "Nigeria",
    "location-ip": "10.x.x.x",
    "location-state": "unkown"
}
```

This can get tricky with logs that have more detail than our example.
And with log sources like email, CASB, network, etc. these logs can
take a very long time to determine what log formats are unique or
repeats.

The json_inspect package is an exploratory/expiramental package to help
flatten these logs and understand what log formats each log source
provides.

## How do you pull that off?

### Comparing full logs
First, we have to be able to compare logs based on structure instead of
content alone.

The way json_inspector compares logs is by converting data into a model
with common values, converting to a string, and then hashing that
string. Then you can safely compare the hashes of the strings.

To dive a little deeper, if there are four-thousand logs that
have the same format (structure, keys, etc.) but different data, then
we will only have to flatten one time to accomodate all four-thousand
logs. For example, the following two JSON objects would be considered
to have an 'identical' model but different data:

```javascript
{
    "name": "John Doe",
    "device": "iPhone X",
    "location": {
        "country": "Nigeria",
        "ip_address": "10.x.x.x",
        "state": "unknown",
    }
}

{
    "name": "Peter Pan",
    "device": "Android",
    "location": {
        "country": "Neverland",
        "ip_address": "192.168.x.x",
        "state": "Imagination",
    }
}
```

The two logs would effectively be covered by the following log model:

```javascript
{
    "name": "STRING",
    "device": "STRING",
    "location": {
        "country": "STRING",
        "ip_address": "STRING",
        "state": "STRING",
    }
}
```

Now what might throw a wrench in this process is if we introduce an
integer or a bool in the "location" object. Then, one log would have an
"INTEGER" or "BOOL" as a value. Then the
hashes of the two objects would no longer match.

Keep in mind the following:
- We care about the structure
- We care about the keys in the object as they can change the
structure.
- All other values that are not an object or list are effectively
equivalent for the purposes of looking at structure.

Since any value that is not an object (dict) or list does not contribute
to the structure of the log, we will replace that data with a common
string, "EDGE". Now using our hashing method, these objects will hash
down to the same hash string.

```javascript
{
    "name": "EDGE",
    "device": "EDGE",
    "location": {
        "country": "EDGE",
        "ip_address": "EDGE",
        "state": "EDGE",
    }
}
```

### Comparing partial logs

If we have logs that we only care about the structure up to a certain
point, then we can provide the same logic as edges but we can convert
dictionaries and lists to common formats to hash and compare.

For dictionaries:

```javascript
{
    "name": "EDGE",
    "device": "EDGE",
    "location": "DICT"
}
```
or
```javascript
{
    "name": "EDGE",
    "device": "EDGE",
    "location": "DICT_KEYS['country', 'ip_address', 'state']"
}
```

For lists:

```javascript
{
    "name": "EDGE",
    "devices": [
        "device1",
        "device2",
        "device3",
    ]
}
```

can convert to

```javascript
{
    "name": "EDGE",
    "devices": ["ALL_EDGES"]
}
```
Likewise,

```javascript
{
    "name": "EDGE",
    "devices": [
        "device1",
        {
            "device2_name": "myDevice",
            "number": "555-555-555"
        }
    ]
}
```

can convert to

```javascript
{
    "name": "EDGE",
    "devices": ["EDGE", "DICT"]
}
```
