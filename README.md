# JSON Inspector

Tool to compare and flatten json-formatted logs for SIEM ingestion.

## Prerequisites

- Install Python 3.6+

## Installation

Create your virtual environment and install dependencies.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Quickstart

```python
from json_inspect import master

m = master.Master(input_file="example_logs.json")
m.make()

m.print_unique_models(resolution=0, indent=2)
m.print_unique_data(resolution=0, indent=2)

m.print_unique_models(resolution=1, indent=2)
m.print_unique_data(resolution=1, indent=2)

m.print_unique_models(resolution=2, indent=2)
m.print_unique_data(resolution=2, indent=2)

m.print_unique_models(resolution=3, indent=2)
m.print_unique_data(resolution=3, indent=2)

m.print_unique_models(resolution=4, indent=2)
m.print_unique_data(resolution=4, indent=2)
```

The output looks like this:

#### Resolution of zero (least granular)

```bash

# RESOLUTION of 0

# m.print_unique_models(resolution=0, indent=2)
{
  "2444e6cb9505d17b89efb154f78a18ea": {
    "age": "edge",
    "assignment": "edge",
    "name": "edge",
    "previous_assignments": "LIST",
    "rank": "edge",
    "species": "edge"
  },
  "672ad685628256d29a5369ebefd059c1": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": "LIST",
    "species": "edge"
  }
}
# m.print_unique_data(resolution=0, indent=2)
{
  "2444e6cb9505d17b89efb154f78a18ea": {
    "age": 43,
    "assignment": "USS Titan",
    "name": "William T. Riker",
    "previous_assignments": "LIST",
    "rank": "Captain",
    "species": "human"
  },
  "672ad685628256d29a5369ebefd059c1": {
    "age": 22,
    "home_planet": "Tatooine",
    "name": "Anakin Skywalker",
    "specialties": "LIST",
    "species": "human"
  }
}
```
#### Resolution of one

```bash
# RESOLUTION of 1

# m.print_unique_models(resolution=1, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": "edge",
    "assignment": "edge",
    "name": "edge",
    "previous_assignments": [
      "DICT(s)"
    ],
    "rank": "edge",
    "species": "edge"
  },
  "91143518648e5077589680d948593883": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": [
      "edges_only"
    ],
    "species": "edge"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": [
      "DICT(s)",
      "edge(s)"
    ],
    "species": "edge"
  }
}
# m.print_unique_data(resolution=1, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": 43,
    "assignment": "USS Titan",
    "name": "William T. Riker",
    "previous_assignments": [
      "DICT",
      "DICT",
      "DICT",
      "DICT",
      "DICT"
    ],
    "rank": "Captain",
    "species": "human"
  },
  "91143518648e5077589680d948593883": {
    "age": 145,
    "home_planet": "Naboo",
    "name": "Jar Jar Binks",
    "specialties": [
      "Screwing things up",
      "Making movies bad"
    ],
    "species": "whocares?"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": 22,
    "home_planet": "Tatooine",
    "name": "Anakin Skywalker",
    "specialties": [
      "Anger",
      "DICT",
      "Pod racing"
    ],
    "species": "human"
  }
}
```

Resolution of two

```bash
# RESOLUTION of 2
# m.print_unique_models(resolution=2, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": "edge",
    "assignment": "edge",
    "name": "edge",
    "previous_assignments": [
      "DICT(s)"
    ],
    "rank": "edge",
    "species": "edge"
  },
  "91143518648e5077589680d948593883": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": [
      "edges_only"
    ],
    "species": "edge"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": [
      "DICT(s)",
      "edge(s)"
    ],
    "species": "edge"
  }
}
# m.print_unique_data(resolution=2, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": 43,
    "assignment": "USS Titan",
    "name": "William T. Riker",
    "previous_assignments": [
      "DICT(s)"
    ],
    "rank": "Captain",
    "species": "human"
  },
  "91143518648e5077589680d948593883": {
    "age": 145,
    "home_planet": "Naboo",
    "name": "Jar Jar Binks",
    "specialties": [
      "edge(s)"
    ],
    "species": "whocares?"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": 22,
    "home_planet": "Tatooine",
    "name": "Anakin Skywalker",
    "specialties": [
      "DICT(s)",
      "edge(s)"
    ],
    "species": "human"
  }
}
```
#### Resolution of three

```bash
# RESOLUTION of 3
# m.print_unique_models(resolution=3, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": "edge",
    "assignment": "edge",
    "name": "edge",
    "previous_assignments": [
      "DICT(s)"
    ],
    "rank": "edge",
    "species": "edge"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": "edge",
    "home_planet": "edge",
    "name": "edge",
    "specialties": [
      "DICT(s)",
      "edge(s)"
    ],
    "species": "edge"
  }
}
# m.print_unique_data(resolution=3, indent=2)
{
  "244c3e15aa13c51c0be4626610baf777": {
    "age": 43,
    "assignment": "USS Titan",
    "name": "William T. Riker",
    "previous_assignments": [
      {
        "assignment": "USS Pegasus",
        "rank": "Ensign"
      },
      {
        "assignment": "USS Potemkin",
        "rank": "Lieutenant"
      },
      {
        "assignment": "USS Hood",
        "rank": "First Officer"
      },
      {
        "assignment": "USS Enterprise-D",
        "rank": "First Officer"
      },
      {
        "assignment": "USS Enterprise-E",
        "rank": "First Officer"
      }
    ],
    "rank": "Captain",
    "species": "human"
  },
  "998db1309e33d4ca6b6b4d0f65758857": {
    "age": 22,
    "home_planet": "Tatooine",
    "name": "Anakin Skywalker",
    "specialties": [
      "Anger",
      {
        "alientating_companions": [
          "Padomay",
          "Obi-Wan Kenobi",
          "Yoda"
        ]
      },
      "Pod racing"
    ],
    "species": "human"
  }
}
```
#### Resolution of four

```bash
# RESOLUTION of 4
# m.print_unique_models(resolution=4, indent=2)
# m.print_unique_data(resolution=4, indent=2)
```

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
