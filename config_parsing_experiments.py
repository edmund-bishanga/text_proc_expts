#!/usr/bin/python

"""
Misc Experiments:
+ config file parsing: ini, yml, json
"""

# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal
# pylint: disable=unused-import

# imports: Std, 3rdParty, CustomLocal
import sys
import time
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from datetime import date, timedelta
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pytest
import yaml
from yaml.loader import SafeLoader

from log_modules.log_gardening import LogGardening

DEF_ENCODING = 'utf-8'

def print_file_contents(filepath):
    with open(filepath, 'r', encoding=DEF_ENCODING) as file:
        content = file.read()
    delim = '++++++++++++++++++++'
    print('\n')
    print(delim)
    print(content)
    print(delim)

def parse_xml_config_file_to_obj(conf_xml_file):
    # REF: https://www.datacamp.com/community/tutorials/python-xml-elementtree
    # parse and return a usable object
    conf_xml_tree = ET.parse(conf_xml_file)
    pprint(conf_xml_tree)
    root = conf_xml_tree.getroot()
    pprint(root)
    print(ET.tostring(root, encoding='utf-8').decode('utf-8'))

    # read/navigate xml tree
    for child in root:
        print(child.tag, child.attrib)

    # read specific xpath detail
    xpath1 = './Stock/retail'
    for item in root.findall(xpath1):
        print(item.tag)
        print(item.text)

    # read specific section: loop through
    for child_item in root.findall('./Stock/*'):
        print(f'{child_item.tag}: {child_item.text}')

    return conf_xml_tree

def parse_ini_config_file_to_obj(conf_ini_file):
    cfg = ConfigParser()
    cfg.read(conf_ini_file)
    print('Config: Sections: ', cfg.sections(), '\n')
    for section in cfg.sections():
        values = [(val, cfg.get(section, val)) for val in cfg.options(section)]
        print(f'Config: section values: {section}: {values}')
    print('\nConfig: param: str: ', cfg.get('build', 'library'))
    print('Config: int: ', cfg.get('operation', 'timeout'))
    print('Config: bool: ', cfg.get('operation', 'offset'))
    return cfg

def parse_yaml_config_file_to_obj(conf_yml_file):
    """ reads a YAML config file: ideally with one config """
    config = {}
    with open(conf_yml_file, 'r', encoding=DEF_ENCODING) as file_obj:
        config = yaml.load(file_obj, Loader=SafeLoader)
        pprint(config, width=120)
    assert config, f'{conf_yml_file}: invalid .yaml config file'
    return config

def get_yaml_config_section_kvs(yaml_config, sect_name):
    err_msg = f'\n"{sect_name}": not in {yaml_config.keys()}'
    # assert sect_name in yaml_config.keys(), err_msg
    if sect_name not in yaml_config.keys():
        print(err_msg)
    return yaml_config.get(sect_name)

def print_yaml_section_values(yml_config, yaml_sections, key_names):
    for sect_name in yaml_sections:
        sect_kvs = get_yaml_config_section_kvs(yml_config, sect_name)
        print(f'\nDEBUG: main: {sect_name}: kvs:')
        pprint(sect_kvs)
        if sect_kvs:
            for item in sect_kvs:
                # print(f'\nDEBUG: section: {sect_name}: item: {item}')
                for key in item.keys():
                    if key in key_names:
                        print(f'section: {sect_name}, item: [{key}: \
                              "{item.get(key)}"]')


def main():
    """ Experiment with Config Parsing. """

    # parse .yaml config file
    yml_files = [
        './configs/example_testbed.yaml',
        './configs/sample_config.yml'
    ]
    for config_yml_file in yml_files:
        yml_config = parse_yaml_config_file_to_obj(config_yml_file)
        print(f'\nDEBUG: main: {config_yml_file}: yml_config_obj')
        pprint(yml_config)
        if 'sample_config.yml' in config_yml_file:
            yaml_sections = ['Build', 'Random', None, '', 'Configure']
            key_names = ['mode', 'logs']
            print_yaml_section_values(yml_config, yaml_sections, key_names)

    # parse .ini config file
    conf_ini_file = './configs/sample_config.ini'
    print_file_contents(conf_ini_file)
    ini_config = parse_ini_config_file_to_obj(conf_ini_file)
    pprint(ini_config.sections())
    for section in ini_config.sections():
        print(repr(section))
        pprint(ini_config.options(section))

    # parse .xml config file
    conf_xml_file = './data/DataSample.xml'
    print_file_contents(conf_xml_file)
    xml_tree_obj = parse_xml_config_file_to_obj(conf_xml_file)
    pprint(xml_tree_obj)

if __name__ == '__main__':
    main()
