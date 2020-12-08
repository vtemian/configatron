configatron
===========

Efficient handling of large configuration files.

## Why?

Handling configuration files can be tricky. Some of those can hit gigabytes in size, their content should be updated in
real-time or as close as possible to real-time. Those constraints shouldn't affect resource consumption or the 
performance of the app using this library.

## What?

Given the above constraints, `configatron` is a simple Python library that can handle a large configuration file without 
storing everything in memory.

## How?

We'll index all configuration groups, by their name. For each group name, store its position within the file and a hash
of its content. Further, build an internal cache for groups and properties, as they are being used.

### Initialization - building index

First, in order to ensure the validity of the configuration, we'll parse the entire file, line by line.
We'll check for valid group names, property names, property types, comments and whitespace placements. At the same time,
we'll build the group index. For now, the index contains only group names and their position within the file.
For now, we don't allow multiple groups with the same name.

### Access - building LRU cache

Since we want to be performant and keep the memory footprint as low as possible, we'll be using an LRU cache. The LRU
cache will store a tuple (<group_name>, <property>) or just (<group_name>, ) as key and a tuple (<value>, <expiration>)
as value. We keep the expiration as well since some properties can be used really often and wouldn't be
evicted from the LRU. 

When a client wants to access a group or property, we'll check the LRU if we have that group.

If not, go to the file and built the specific group (since we know its position, no need to parse the entire file).
The file could have been changed, so we'll need to check if the content of that specific group hasn't been affected
(by reading the specific bytes and build a hash from them). If the current hash group (the hash that is store in the
initial index) and the newly computed hash don't match, we'll need to re-index the entire file.
The same logic occurs if the group or the property is considered expired.

# TODO:
 - [x] multiple groups with the same name, throw exception
 - [x] invalid syntax should throw exception 
 - [x] implement overrides
 - [ ] documentation
   - [ ] drawing scheme
   - [ ] more details on readme
   - [ ] code comments
 - [ ] tests
   - [x] makefile
   - [x] ci/cd
   - [x] check formatting
   - [x] invalid syntax
   - [x] valid syntax
   - [ ] unit tests
   - [ ] performance tests
   - [ ] overrides
