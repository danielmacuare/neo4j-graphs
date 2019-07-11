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


def parse_yaml(yaml_file=None):
    if yaml_file:
        with open(yaml_file, 'r') as nodes_yaml:
            try:
                nodes_dict = yaml.safe_load(nodes_yaml)
                return nodes_dict
            except yaml.YAMLError as err:
                print(err)
    else:
        print(f'** ERROR: Please pass a yaml file to the function')
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
                # ipdb.set_trace()
                device = properties['name']
                print(f'Creating "{node_id}" as a "{label}" Node')
                neo_nodes = Node(label, **properties)
                graph.create(neo_nodes)
                print(f'{node_id}.name = "{device}" Node has been '
                      f'created in the DB.\n')
            else:
                print(f'** ERROR: The {node_id.upper()} node must contain a '
                      f'property called "name".\n\n')
    return None


def get_relationship_properties(rel_properties):
    """ 
    Takes a dictionary with the relationship properties, like:
    {'from': {'label': 'Subnet', 'name': '10.171.0.0/19'},
     'label': 'PART_OF',
     'label_prop': {'cost': 5, 'created_on': '12/06/19'},
     'to': {'attached_to': 'man2-rc-int240-cl1', 'label': 'SecZone', 'name': 'LAN'}}   

    Returns a tupple with 2x dictionaries from_properties and to_properties
    """
    for prop_names, prop_values in rel_properties.items():
        # pprint(prop_names)
        # pprint(prop_values)
        if prop_names == 'from':
            from_properties = prop_values.copy()
            from_properties.pop('label')
            print(from_properties)
        if prop_names == 'to':
            to_properties = prop_values.copy()
            to_properties.pop('label')
            print(to_properties)
    return(from_properties, to_properties)


def create_relationships(relationships_dict):
    data = relationships_dict
    for rel_type, rel_name in data.items():
        # pprint(rel_type)
        # pprint(rel_name)
        for rel_desc, rel_properties in rel_name.items():
            # pprint(rel_desc)
            # pprint(rel_properties)
            relation = rel_properties['label']
            relation_label = rel_properties['label_prop']
            print(relation_label)
            # ipdb.set_trace()
            from_label = rel_properties['from']['label']
            to_label = rel_properties['to']['label']
            from_properties, to_properties = get_relationship_properties(rel_properties)
            from_node = Node(from_label, **from_properties)
            to_node = Node(to_label, **to_properties)
            create_relation = Relationship(from_node, relation, to_node, **relation_label)
            graph.create(create_relation)

    return None


if __name__ == '__main__':
    # Secure Way
    # password = getpass('Please input the password to connect to the DB: ')
    # graph = Graph('http://127.0.0.1:7474', user='neo4j', password='neo4lab')

    graph = Graph('bolt://127.0.0.1:7687', user='neo4j', password='neo4lab')
    delete_db(graph)
    nodes_dict = parse_yaml('nodes.yaml')
    relationships_dict = parse_yaml('relationships.yaml')
    pprint(relationships_dict)
    create_nodes(nodes_dict)
    create_relationships(relationships_dict)

    sys.exit()
