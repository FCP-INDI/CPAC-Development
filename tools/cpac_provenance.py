'''Utility to generate an SVG from provenance information in a C-PAC
sidecar file

Commandline usage: CpacProvenance $PATH_TO_SIDECAR.json'''
import json
import os
from sys import argv, exit as sys_exit
from itertools import chain
import graphviz
from matplotlib.pyplot import rcParams

COLORS = rcParams['axes.prop_cycle'].by_key()['color']


class Prop():
    '''Class to hold a provenance graph property'''
    name: str
    parent: 'Entity'

    def __init__(self, parent, prop):
        self.name = prop
        self.parent = parent

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    def color(self):
        '''Method to get a prop's color for a given entity'''
        _color = COLORS[list(self.parent.props.keys()).index(str(self)) %
                        len(COLORS)]
        return f'"{_color}"'


class Entity():
    '''Class to hold a provenance graph entity'''
    node: str
    props: dict

    def __new__(cls, entities, prov_string=None):
        entity = super().__new__(cls)
        entity.props = {}
        if prov_string is None:
            entity.node = ''
            return entity
        prop, entity.node = prov_string.split(':', 1)
        if entity.node in entities:
            entities[entity.node].add_prop(prop)
        else:
            if prop:
                entity.props[prop] = Prop(entity, prop)
            entities[entity.node] = entity
        return entities[entity.node]

    def __repr__(self):
        if self.props and any(self.props):
            return ' '.join([
                f'"{self.node}"',
                '[label="{' + self.node + ' |{',
                ' | '.join([
                    '<' + prop + '> ' + prop for prop in self.props
                ]) + '}}"]'])
        return f'"{self.node}"'

    def __str__(self):
        return self.__repr__()

    def add_prop(self, prop):
        '''Method to add a property to an entity'''
        if prop not in self.props:
            self.props[prop] = Prop(self, prop)


class Connection():
    '''Class to store provenance graph connection information'''
    connect_from: 'Entity'
    connect_on: str
    connect_to: 'Entity'

    def __new__(cls, entities, connections, provenance_pair=None):
        connection = super().__new__(cls)
        connection.connect_from = Entity(entities)
        connection.connect_on = ''
        connection.connect_to = Entity(entities)
        if provenance_pair is not None:
            if not isinstance(provenance_pair[1], str):
                raise Exception(provenance_pair)
            if isinstance(provenance_pair[0], (list, tuple)):
                for provenance_item in provenance_pair[0]:
                    connection = Connection(entities, connections,
                                            (provenance_item,
                                             provenance_pair[1]))
                    connections.add(str(connection))
            elif isinstance(provenance_pair[0], str):
                connection.connect_from, connection.connect_to = [
                    Entity(entities, provenance_item) for provenance_item in
                    provenance_pair]
                connection.connect_on = provenance_pair[0].split(':', 1)[0]
                connections.add(str(connection))
        return connection

    def __repr__(self):
        return (f'"{self.connect_from.node}":"{self.connect_on}" -> "'
                f'{self.connect_to.node}" [color='
                f'{self.connect_from.props[self.connect_on].color()}];')

    def ___str___(self):
        return self.__repr__()


def graph_provenance(sidecar_file, gv_format='svg'):
    '''
    Function to generate a visual provenance graph from a C-PAC sidecar

    Parameters
    ----------
    sidecar_file : str
        path to C-PAC provenance file

    gv_format : str
    '''
    with open(sidecar_file, 'r', encoding='utf-8') as file:
        sidecar = json.load(file)
    graph_file = '.'.join([
      os.path.basename(sidecar_file)[::-1].split('.', 1)[1][::-1],
      'provenance'])
    graphviz.Graph(graph_file,
                   make_connections(sidecar['CpacProvenance']),
                   format=gv_format,
                   engine="dot"
                   ).unflatten(stagger=len(sidecar['CpacProvenance'])).render()
    for suffix in ['', '.2.svg']:
        try:
            os.remove(f'{graph_file}.gv{suffix}')
        except FileNotFoundError:
            pass
    print(f'Created `{graph_file}.gv.{gv_format}`.')


def make_connections(provenance_list, output=True, entities=None,
                     connections=None):
    '''Function to genrate a DOT graph from CpacProvenance syntax

    Parameters
    ----------
    provenance_list : list

    output : boolean

    entities : dict or None

    conections : set or None

    Returns
    -------
    str
    '''
    if entities is None:
        entities = {}
    if connections is None:
        connections = set()
    plc = provenance_list[:]
    leaf = plc.pop()
    if plc:  # pylint: disable=too-many-nested-blocks
        make_connections(plc, False, entities, connections)
        if isinstance(leaf, str):
            if isinstance(plc[:-1], str):
                Connection(entities, connections, (plc[:-1], leaf))
            else:
                if isinstance(plc[-1], str):
                    Connection(entities, connections, (plc[-1], leaf))
                else:
                    for sublist in plc:
                        make_connections(sublist, False, entities, connections)
                        if isinstance(sublist[-1], str):
                            Connection(entities, connections,
                                       (sublist[-1], leaf))
                        else:
                            Connection(entities, connections, (list(
                                chain.from_iterable(sublist))[-1], leaf))
            if output and isinstance(leaf, str):
                Connection(entities, connections, (leaf, ":outputs"))
                return '\n'.join([f'{line};' if not any(
                    line.endswith(char) for char in [';', '{', '}']
                ) else line for line in [
                    f'\ndigraph "{Entity(entities, leaf).node}"' + ' {',
                    *[f'  {line}' for line in [
                        'node [shape=record fontsize="12pt"];',
                        *list(set(
                          str(entity) for _, entity in entities.items())),
                        *[connection for connection in connections if
                          connection != '"":"" -> "";']
                    ]],
                    '}']])
    return ''


def print_usage(and_exit=True):
    '''Function to display commandline usage'''
    header = ''
    with open(os.path.join(os.path.dirname(__file__), os.pardir,
                           'bin/CpacProvenance'),
              'r', encoding='utf-8') as bin_file:
        for line in bin_file.readlines():
            if line.startswith('# '):
                header += line[2:]
            else:
                break
    print(header)
    if and_exit:
        sys_exit(0)


if __name__ == '__main__':
    if len(argv) != 2 or not os.path.exists(argv[1]):
        print_usage()
    graph_provenance(argv[1])
