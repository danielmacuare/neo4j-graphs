#!/usr/bin/env python3
import sys

'''
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


def yaml_to_python(yaml_file=None):
    if yaml_file:
        with open(yaml_file, 'r') as yaml_data:
            try:
                py_data = yaml.safe_load(yaml_data)
                return py_data
            except yaml.YAMLError as err:
                print(err)
    else:
        print('A file has not been passed to the function yaml_to_python()')
        return None


def delete_db(graph):
    print('Cleaning the Database')
    graph.delete_all()
    return None


def create_nodes(node_label='Firewall', **kwargs):
    '''
    This function will receive:
    - A string with the node label.
    - A dictionary with the all teh properties of the node.
    '''
    if kwargs.get('name'):
        #for properties in kwargs:
        print(f'Creating "{device.upper()}" as a "{node_label.upper()}" Node')

        neo_nodes = Node(node_label, **kwargs)
        graph.create(neo_nodes)

        print(f'The "{device.upper()}" Node has been successfully created '
              f'in the DB\n\n')
    else:
        print(f'ERROR: The {device.upper()} node must contain a property '
              f'called "name"\n')


if __name__ == '__main__':

    nodes = yaml_to_python('nodes.yaml')
    #pprint(nodes)
    #password = getpass('Please input the password to connect to the DB: ') #Secure Way
    graph = Graph('bolt://127.0.0.1:7687', user='neo4j', password='neo4lab')
    #graph = Graph('http://127.0.0.1:7474', user='neo4j', password='neo4lab')
    delete_db(graph)

# TO_DO - Pass this to the create_nodes function.
    #ipdb.set_trace()
    for label, content in nodes.items():
        for device, properties in content.items():
            #print(label)
            #print(device)
            #print(properties)
            create_nodes(label, **properties)

    sys.exit()
