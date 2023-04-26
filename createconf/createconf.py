"""
createconf - Create config files from templates and data

This script generates configuration files using Mako templates and JSON data.
Users can provide template files, JSON data (either as a string or a file path),
and optionally default JSON data. The script also supports filtering out specific
keys from the JSON data and checking for duplicate keys.

Usage:
  python createconf.py [options]

Options:
  -d, --data                   JSON data as a string or file path (default: '')
  -D, --defaults               Filepath to default JSON data (default: '')
  -t, --template               Template filepath (default: ./templates/cisco_conf.mako)
  -i, --ignore_keys            List of keys to ignore or filter out (default: [])
  -o, --outfile                File path to write the output (default: prints to stdout)
  -v, --verbose                Enable verbose output (default: False)
  -I, --ignore_duplicate_keys  Disable checking for duplicate keys (default: True)
"""
import argparse
import os
import sys
import json
from collections import defaultdict
from mako.template import Template

class DuplicateKeyError(Exception):
    """Raised when duplicate keys are found in JSON data."""

def parse_args():
    """Parse command-line arguments for the createconf script."""
    parser = argparse.ArgumentParser()
    # Create the argument parser and add arguments
    parser = argparse.ArgumentParser(description="Configs")
    parser.add_argument(
        "-d", "--data", type=str, required=True,
        help="""Data in json format or a file path to a json file. examples:
        ./createconf.py --data '{\"hostname\":\"switch-01\", \"interface Ethernet1/1\": {\"description\": \"Eth 1/1\", \"switchport mode\":\"trunk\"}}'
        OR: ./createconf.py --data ./mydata.json"""
    )
    parser.add_argument("-D", "--defaults", type=str, default='',
                        help="Path to default data, eg ./defaults.json")
    parser.add_argument("-t", "--template", type=str,
                        default = os.path.join(os.path.dirname(__file__),
                        "templates", "cisco_conf.mako"), 
                        help="Path to the mako template, eg. --template ./config.mako")
    parser.add_argument("-i", "--ignore_keys", type=str, nargs='+', default=[],
                        help="A list of keys to ignore/filter. Eg: 'feature lacp' 'line vty' ")
    parser.add_argument("-o", "--outfile", type=str, help="Write to a file. Eg. --target ./config")
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose output")
    parser.add_argument("-I", "--ignore_duplicate_keys", action='store_false',
                        help="Don't check for duplicate keys in data or defaults")
    return parser.parse_args()

def deep_merge(dict1, dict2):
    """Recursively merge two dictionaries, with values from dict2 taking precedence.
    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.
    Returns:
        dict: The merged dictionary.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def warn_on_duplicate_keys(ordered_pairs):
    """Raise an error if duplicate keys are found in a list of key-value pairs."""
    counter = defaultdict(int)
    result = {}
    for key, value in ordered_pairs:
        if counter[key] > 0:
            raise DuplicateKeyError(f"Duplicate key '{key}' found.")
        counter[key] += 1
        result[key] = value
    return result

def load_data(data: str, strict: bool) -> dict:
    """Load JSON data from a string or file."""
    try:
        if os.path.exists(data):
            with open(f"{data}",'r',encoding='utf-8') as data_file:
                if strict:
                    data = json.load(data_file, object_pairs_hook=warn_on_duplicate_keys)
                else: data = json.load(data_file)
        else:
            if strict:
                data = json.loads(data, object_pairs_hook=warn_on_duplicate_keys)
            else: data = json.loads(data)
        return data
    except DuplicateKeyError as dke:
        raise dke
    except FileNotFoundError:
        print(f"Error: File not found - data: {data}")
        sys.exit(1)
    except json.decoder.JSONDecodeError as decoder_error:
        print(f"Error loading json data - data: {data}:\n  {decoder_error}")
        sys.exit(1)

def filter_data(data: dict, ignore: list, verbose: bool) -> dict:
    """Remove specified keys from a dictionary."""
    for i in ignore:
        if i in data:
            if verbose:
                print(f"INFO: Ignoring key: '{i}'.")
            del data[i]
        else:
            if verbose:
                print(f"WARN: Trying to ignore '{i}' - but key not found in template.")
    return data

def createconf(args):
    """Generate a configuration file from a template and JSON data."""
    data = load_data(args.data, args.ignore_duplicate_keys)

    # Create a Template object with the loaded template string
    with open(args.template, "r", encoding='utf-8') as template_file:
        template_str = template_file.read()
    template = Template(template_str)
    defaults = {}
    if args.defaults:
        defaults = load_data(args.defaults, args.ignore_duplicate_keys)
    data_f = deep_merge(defaults, data)

    # Filter unwanted keys
    data_filtered = filter_data(data_f, args.ignore_keys, args.verbose)

    # Render the template with your variables
    output = template.render(data={**data_filtered})

    # Write output
    if args.outfile:
        with open(args.outfile, "w", encoding='utf-8') as write_file:
            write_file.write(output)
            write_file.close()
        print(f"Configuration written to {args.outfile}")
        if args.verbose:
            print(output)
    else:
        print(output)

if __name__ == '__main__':
    createconf(parse_args())
