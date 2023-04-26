# createconf

[![Python CI](https://github.com/zoojar/createconf/actions/workflows/python-ci.yml/badge.svg)](https://github.com/zoojar/createconf/actions/workflows/python-ci.yml)

createconf is a command-line tool that generates configuration files from templates and data. It uses Mako templates to create the desired output, which can then be applied to various devices or services.

## Table of contents
- [createconf](#createconf)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Troubleshooting](#troubleshooting)
  - [Advanced Usage](#advanced-usage)
  - [Customizing Templates](#customizing-templates)
  - [Ordering in createconf](#ordering-in-createconf)
  - [Testing](#testing)


## Installation
To install the required libraries for createconf, run the following command:

`pip install mako`

## Basic Usage

To run createconf, use the following command:

`python createconf.py [options]`

### Options

The following options can be used with createconf:

`-d`, `--data` : Provide data in JSON format or a file path to a JSON file. Default value is `./example-data.json`.

`-D`, `--defaults` : Path to default data (e.g., `--defaults ./defaults.json`).

`-t`, `--template` : Path to the Mako template (e.g., `--template ./config.mako`). Default value is `./templates/cisco_conf.mako`.

`-i`, `--ignore_keys` : A list of keys to ignore/filter from the config.

`-o`, `--outfile` : Write to a file (e.g., `--target ./config`).

`-v`, `--verbose` : Verbose output

`-I`, `--ignore_duplicate_keys` : Don't check for duplicate keys in data or defaults.

### Examples

Using inline JSON data:

`./createconf.py --data  '{\"hostname\":\"switch-01\", \"interface Ethernet1/1\": {\"description\": \"Eth 1/1\", \"switchport mode\":\"trunk\"}}'`

The `--data` flag is provided with inline JSON data that contains the configuration for the `hostname` and `interface Ethernet1/1`.

Based on the default Mako template (`cisco_conf.mako`), createconf will generate the following configuration output:

```
hostname switch-01
interface Ethernet1/1
  description Eth 1/1
  switchport mode trunk
```

Using a JSON file:

`./createconf.py --data ./mydata.json`

Writing output to a file:

`./createconf.py --data ./mydata.json --outfile ./config`

### Data, templating and Cisco commands

createconf utilizes Mako templates (with `./templates/cisco_conf.mako` as the default template) along with hierarchical JSON data to generate customizable and granular Cisco configurations. By merging default and user-specified configurations, users can maintain default settings while making device-specific adjustments. The accurate representation of Cisco commands and their sub-commands within the JSON data structure is essential for creating precise and effective network device configurations through Mako templates.

Let's consider an example where you have a default JSON configuration file and a user-specific JSON configuration file. The goal is to show how the granularity of a sub-command and key string can allow you to override specific values while maintaining the default settings.

Default JSON configuration (`defaults.json`):

```json
{
    "interface Ethernet1/1": {
        "switchport mode": "access",
        "switchport access vlan": "10"
    },
    "interface Ethernet1/2": {
        "switchport mode": "trunk",
        "switchport trunk allowed vlan": "1-100"
    }
}
```

User-specific JSON configuration (`user_data.json`):

```json
{
    "interface Ethernet1/1": {
        "switchport access vlan": "20"
    },
    "interface Ethernet1/2": {
        "switchport trunk allowed vlan": "1-50"
    }
}
```

In this example, the user-specific JSON configuration file overrides the default configuration for `interface Ethernet1/1` and `interface Ethernet1/2`. The key string `"switchport access vlan"` for `interface Ethernet1/1` has a new value `"20"` in the user-specific configuration, while `"switchport trunk allowed vlan"` for `interface Ethernet1/2` is changed to `"1-50"`.

After merging the default and user-specific configurations, the resulting JSON data would look like this:

```json
{
    "interface Ethernet1/1": {
        "switchport mode": "access",
        "switchport access vlan": "20"
    },
    "interface Ethernet1/2": {
        "switchport mode": "trunk",
        "switchport trunk allowed vlan": "1-50"
    }
}
```

The createconf tool, using Mako templates, generates a configuration based on this merged JSON data. The granularity of the sub-commands and key strings allows for specific values to be overridden while preserving the other default settings.


### How data types are parsed with cisco_conf.mako

The default mako template `cisco_conf.mako` handles the way data is parsed and processed according to the data types of the values in the JSON configuration. The primary data types used within the JSON data structure are Strings, Lists, and Maps/Dicts. Understanding the rules around these data types and how they are parsed is crucial for creating valid and accurate configurations.

#### Strings ""

Strings are still used to represent simple values or commands in the JSON configuration. When parsed, a String is directly rendered as a part of the parent command. For example:

```json
{
    "hostname": "network-device"
}
```

The resulting configuration:
`hostname network-device`

#### Lists []

Lists are used to represent multiple values for a single command. When parsed, the List items are joined together with a space and appended to the parent command. For example:

```json
{
    "switchport trunk allowed vlan": ["10", "20", "30"]
}
```

The resulting configuration:
`switchport trunk allowed vlan 10 20 30`

In this example, the List is used to specify multiple VLANs allowed on a trunk port. The Mako template processes the List and generates a single configuration line with all VLANs included as space-separated values.

#### Maps {}

Maps (or Dictionaries) are used to represent hierarchical command structures, where a parent command has multiple sub-commands. When parsed, the key represents the parent command, and the value (a nested Map/Dict) represents its sub-commands. The parsing process is recursive, allowing for multiple levels of nesting. For example:

```json
{
    "interface vlan112": {
        "ip address": "172.16.112.4/24",
            "hsrp 112": {
                "priority": "112",
                "ip": "172.16.112.1"
            }
    }
}
```

The resulting configuration:
```
interface vlan112
  ip address 172.16.112.4/24
    hsrp 112
      priority 112
      ip 172.16.112.1
```

## Troubleshooting

If you encounter any issues while using createconf, ensure that you have the required libraries installed and that the provided JSON data is valid. If problems persist, use the `--verbose` flag to obtain more information about the issue.

## Advanced Usage

### Merging Default and Custom Data

createconf allows you to merge default data with custom data. This can be useful when you have a set of default configurations that you want to apply to multiple devices or services, but you also want to provide custom data for specific instances. To merge default and custom data, use the `--defaults` option:

`./createconf.py --defaults ./defaults.json --data ./custom-data.json`

### Filtering Unwanted Keys

You can filter out specific keys from the input data using the `--ignore_keys` option. This can be useful when you want to exclude certain configurations from the output. To ignore specific keys, pass a space-separated list of keys to the `--ignore_keys` option:

`./createconf.py --data ./data.json --ignore_keys 'key1' 'key2'`

### Duplicate Key Handling

By default, createconf checks for duplicate keys in the input data and raises an error if any are found. If you want to allow duplicate keys in your input data, you can disable this check using the `--ignore_duplicate_keys` option:

`./createconf.py --data ./data.json --ignore_duplicate_keys`

## Customizing Templates

createconf uses Mako templates to generate output. You can customize these templates to suit your specific needs. Mako templates allow you to embed Python code within your templates, providing you with a powerful tool to create dynamic content.

For more information on how to create and customize Mako templates, refer to the [Mako documentation](https://docs.makotemplates.org/en/latest/).

## Ordering in createconf

Ordering can be an important aspect when working with createconf, especially when dealing with configuration files that require a specific order for proper execution. There are several areas where ordering may be relevant, including the order of the input data, the order of the rendered template output, and the order in which default and custom data are merged.

When providing input data to createconf, ensure that your data is organized in the correct order, as required by your templates and the target configuration file format. JSON, being the default input data format for createconf, does not guarantee key ordering. However, createconf uses the `collections.defaultdict` module to maintain the key order as they appear in the input JSON data.

The order of the rendered output depends on the structure of your Mako templates. To ensure the correct order in your generated configuration files, carefully design your templates, keeping the target configuration format's ordering requirements in mind. The Mako template engine allows you to control the output order by organizing your template code accordingly.

### Merging Default and Custom Data

When using the `--defaults` option to merge default data with custom data, createconf performs a deep merge of the dictionaries. The order in which keys and values are merged depends on the order of the input data. Custom data takes precedence over default data, so if a key exists in both default and custom data, the custom data's value will be used.

In summary, when working with createconf, be mindful of ordering requirements for your specific use case, and structure your input data and templates accordingly to ensure the proper order is maintained in the generated configuration files.


## Testing

Unit tests are located in ./tests

To run the tests, use the following command:

`py -m unittest discover tests`