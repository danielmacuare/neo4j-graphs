#!/usr/bin/env python3
import sys

'''
TO-DO:
logging

The following module has basic functions to:
Create_nodes()
Delete_nodes()
Modify_nodes()
Create_relationships()
'''
from py2neo import Graph, Node, Relationship
from getpass import getpass
from pprint import pprint
import ipdb
import sys
import yaml


def delete_db(graph):
    print('Cleaning the Database')
    graph.delete_all()
    return None


def yaml_to_python(yaml_file=None):
    if yaml_file:
        with open(yaml_file, 'r') as nodes_yaml:
            try:
                nodes_dict = yaml.safe_load(nodes_yaml)
                return nodes_dict
            except yaml.YAMLError as err:
                print(err)
    else:
        print(f'ERROR: A file has not been passed to the function '
              f'yaml_to_python()')
        return None


def create_nodes(nodes_dict):
    '''
    This function will receive:
    - A dictionary with the nodes and all its properties and will create
    a graph.
    Next, you can find the structure of the dictionary:
{'FW': {'FW-A': {'commisioned_on': '26/07/19',
                 'location': 'lhr4',
                 'name': 'FW-A'},
        'FW-B': {'commisioned_on': '25/07/17',
                 'location': 'ams4',
                 'text': 'FW-B'},
        'FW-C': {'commisioned_on': '25/01/16',
                 'location': 'man2',
                 'name': 'FW-C'}},
 'SUBNET': {'10.171.0.0/19': {'host_grp': 'MAN OFFICES',
                              'name': '10.171.0.0/19'},
            '10.177.0.0/16': {'host_grp': 'AMS4 PROD', 'name': '10.171.0.0/16'},
            '10.184.0.0/14': {'host_grp': 'LHR4 PROD', 'name': '10.184.0.0/16'},
            '10.204.0.0/16': {'host_grp': 'AWS PROD', 'name': '10.204.0.0/16'}}}
    '''
    for label, content in nodes_dict.items():
        for node_id, properties in content.items():
            # print(label)
            # print(node_id)
            # print(properties)
            if properties.get('name'):
                #ipdb.set_trace()
                device = properties['name']
                print(f'Creating "{node_id.upper()}" as a '
                      f'"{label.upper()}" Node')
                neo_nodes = Node(label, **properties)
                graph.create(neo_nodes)
                print(f'{label.upper()}.name = "{device.upper()}" Node has been successfully '
                      f'created in the DB.\n')
            else:
                print(f'** ERROR: The {node_id.upper()} node must contain a '
                      f'property called "name".\n\n')
    return None


if __name__ == '__main__':
    # Secure Way
    # password = getpass('Please input the password to connect to the DB: ') 
    # graph = Graph('http://127.0.0.1:7474', user='neo4j', password='neo4lab')

    graph = Graph('bolt://127.0.0.1:7687', user='neo4j', password='neo4lab')
    delete_db(graph)
    nodes_dict = yaml_to_python('nodes.yaml')
    # pprint(nodes)
    create_nodes(nodes_dict)

    sys.exit()
