# Testfile-suite
A lightweight, fast, and customizable command-line tool for generating hierarchical test-file directories. 

## Overview
`testfile-suite` is designed to rapidly build out mock directory structures populated with randomized Base64-encoded text files. It is configurable, allowing developers to simulate complex file system scenarios for testing I/O, recursion performance, backup tools, or directory traversing scripts.

## Usage
The tool runs off a single python script (`main.py`) which acts as the entry point and accepts several configuration parameters to shape the output tree. 

```bash
python3 main.py --depth [INT] --breadth [INT] [OPTIONS]
```

### Required Arguments
* `--depth`: The depth of the recursive tree. This determines how many levels of sub-folders the script will generate downwards. 
* `--breadth`: The number of files and folders to create at **each** level of the tree.

### Optional Arguments
* `--size`: Target size of each generated text file in Kilobytes (KB). Defaults to `1.0`. The script calculates and writes randomized `os.urandom` byte data encoded as Base64 strings to approximate this file weight. 
* `--path`: Base output path to spawn the root of the test tree in. Defaults to the current active directory (`.`).

## Example Use Cases
Generate a simple 3-tier deep nested structure (3 folders each containing 3 folders) where each folder contains 3 files at 1.5KB each: 
```bash
python3 main.py --path ./my_test_tree --depth 3 --breadth 3 --size 1.5
```
