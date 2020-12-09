configatron
===========

`configatron` is a Python library that can handle a large configuration file without 
storing everything in memory. It supports near real-time configuration updates.

## Installation

Prerequisites:
  * Python 3.6+

###### Private repository

```bash
python3 -m pip install https://github.com/vtemian/configatron.git
```

###### Local

```bash
tar -xzf configaron.tar.gz && cd configatron/
python3 -m pip -e .
```

## Usage

Initial file reading won't block.

```python3
from configatron import Configatron

config = Configatron("/path/to/config")
config.get("group").get("property")
```

Specify configuration overrides.

```python3
config = Configatron("/path/to/config/overrides", ["production", "ubuntu"])
```

Control LRU cache options.

```python3

cache_options = {
    "size": 10000,        # number of items in cache, default 10 000 items
    "lifespan": 60 * 60,  # seconds for each item in cache, default 1h
}
config = Configatron("/path/to/config/overrides", cache_options=cache_options)
```

Don't validate on the initial index (default `True`).

```python3
config = Configatron("/path/to/config/overrides", validate=False)
```

## Development

Install development dependencies
```bash
pip install -r requirements.dev.txt
```

Run tests
```bash
make tests
```

Run code format
```bash
make fmt
```

Check for formatting issues
```bash
make check-fmt
```

## Implementation

We'll index all configuration groups, by their name. For each group name, store its position within the file and a hash
of its content. Further, build an internal cache for groups and properties, as they are being used. Detect changes
and re-index if necessary.

```
[group-1]
  ....
[group-2] <----+ seek to position
  ....
  ....
  ....    <----+ sha256 content
  ....

[group-n]
```

### Initialization - building index

First, in order to ensure the validity of the configuration, we'll parse the entire file, line by line.
We'll check for valid group names, property names, property types, comments and whitespace placements. At the same time,
we'll build the group index. For now, the index contains only group names and their position within the file.
We don't allow multiple groups with the same name.

### Access - building LRU cache

Since we want to be performant and keep the memory footprint as low as possible, we'll be using an LRU cache. The LRU
cache will store a <group_name> as key, and a tuple (<value>, <expiration>) as value. We keep the expiration as 
well since some properties can be used really often and wouldn't be evicted from the LRU, thus making it impossible to
update them without a full restart.

When a client wants to access a group or a property, we'll ask the LRU cache if we have that group.

If not, go to the file and built the specific group (since we know its position, no need to parse the entire file).
The file could have been changed, so we'll need to check if the content of that specific group hasn't been affected
(by reading the specific bytes and build a hash from them). If the current hash group (the hash that is store in the
initial index) and the newly computed hash don't match, we'll need to re-index the entire file.
The same logic occurs if the group or the property is considered expired.

A full index triggers a cache purge as well since we don't want to have stale data. The cache size and items lifespan
are configurable, depending on usage.

### Architecture

```
                   +---------------+
                   |               |
       +-----------+  Configatron  +------------+
       |           |               |            |
       |           +---------------+            |
       |                                        |
       |                                        |
       |                                        |
       |                                        |
+------v------+                          +------v------+
|             |                          |             |
|  LRUCache   |                +---------+   Indexer   |
|             |                |         |             |
+-------------+                |         +------+------+
                               |                |
                          +----v----+           |            +---------+
                          |         |           |            |         |
                          | Scanner |           +----------->+ Group#1 |
                          |         |           |            |         |
                          +----+----+           |            +----+----+
                               |                |                 |        +------------+
                               |                |                 |        |            |
                               |                |                 +------->+ Property#1 |
                          +----v---+            |                 |        |            |
                          |        |            |                 |        +------------+
                          | Reader |            |                 |
                          |        |            |                 |        +------------+
                          +--------+            |                 |        |            |
                                                |                 +------->+ Property#2 |
                                                |                          |            |
                                                |                          +------------+
                                                |
                                                |            +---------+
                                                |            |         |
                                                +----------->+ Group#2 |
                                                             |         |
                                                             +---------+
```

As a high-level architecture, as state previously, the two main components are the `LRUCache` and the `Indexer`.
The `LRUCache` just holds objects and evict expired or not so often accessed items.
The `Indexer` holds the groups and the mean to create and refresh them. It delegates this job to the `Scanner` that
interact with `Nodes` (`Groups`, `Property` and `Comments`). It doesn't know how to build it, but it knows their 
hierarchy (how groups interacts with properties and comments). `Scanner` doesn't read itself the file content, but it
uses the `Reader` for that.

Following this structure is easy to use another medium for file storage (remote/bucket/url/stdin). We just need to 
create a different `Reader` for it. Updating the hierarchy between nodes or adding new node types is fairly easy.
We just need to adapt the scanner and for each node, describe how it should be parsed.

Right now, each element knows how to build itself. It does that by defining two methods (`is_valid` and `parse`) and
defining a regex used to check if we can build the element from the current line.

### Alternative considerations and improvements

##### Parsing
Right now, parsing is done using regex, which is always messy, hard to maintain and understand, can throw hard to
debug bugs, performance issues, infinite loops etc.

LR parsers can be used in this case. There are known pure Python [libraries](https://wiki.python.org/moin/LanguageParsing)
that implements those kinds of parsers, well tested and open-source. Building and maintaining grammar is way easier
than maintaining regular expressions.

Python also has a built-in library that can parse ini files. It's not that efficient since it loads the entire file
in memory, but some components can be re-used.

#### LRU

The current LRU implementation is from scratch. In production, we can use an open source library since those are 
already battle tested and more optimized. The current implementation uses an OrderDict, thus making it sub-optimal.

#### <10Mb file sizes

For small size files, we can keep everything in-memory and have an instant access, without a caching mechanism. With a 
mechanism for on-demand indexing we would re-index the file when asked by our users.

### Code quality

#### Testing

Having complex logic for indexing, caching and parsing, I thought that the safest way to test it would be in integration.
For that, the majority of test cases are parsing and indexing config files, written in temporary files. There are more
than 110 tests.

#### Style

The codebase is format using `black`, documented and type annotated.

#### CI

Github actions are being used to check for formatting errors and run tests.
