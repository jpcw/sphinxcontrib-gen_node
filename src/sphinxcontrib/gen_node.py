# -*- coding: utf-8 -*-
"""
    sphinx.ext.gen_node
    ~~~~~~~~~~~~~~~

    Allow gen_nodes to be inserted into your documentation.  Inclusion of gen_nodes can
    be switched of by a configuration variable.  The gen_nodelist directive collects
    all gen_nodes of your project and lists them along with a backlink to the
    original location.

    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes

from sphinx.locale import _
from sphinx.environment import NoUri
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive, make_admonition


NODES = {}
LISTED = 'list'


class MetaNode(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)


class BaseNode(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])
        ad = make_admonition(NODES[self.name.lower()]['node_adm'],
                             self.name, [_(self.name)], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)
        set_source_info(self, ad[0])
        return [targetnode] + ad


class BaseNodeList(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        bcls = NODES[self.name[0:-len(LISTED)].lower()]['node_gen']
        return [bcls('')]


def setup_nodes(config_nodes):

    for desired_node in config_nodes:
        elt = {}
        elt['name'] = desired_node[0].title()
        elt['namelist'] = '%s%s' % (desired_node[0].title(), LISTED.title())
        globals()[desired_node[0]] = MetaNode(desired_node[0],
                                             (nodes.Admonition,
                                              nodes.Element), {})
        elt['node_adm'] = globals()[desired_node[0]]
        elt['env_all'] = '%s_all_gen_nodes' % desired_node[0]
        elt['show_list'] = desired_node[1]
        elt['group_title_doc'] = desired_node[2]
        elt['show_desc_paragraph'] = desired_node[3]
        globals()['%s%s' % (desired_node[0], LISTED)] = MetaNode('%s%s' % (desired_node[0], LISTED),
                                                        (nodes.General,
                                                         nodes.Element), {})
        elt['node_gen'] = globals()['%s%s' % (desired_node[0], LISTED)]
        elt['meta_dir'] = MetaNode(elt['name'], (BaseNode,), {})
        elt['meta_dirlist'] = MetaNode(elt['namelist'],
                                               (BaseNodeList,),
                                               {})
        NODES[desired_node[0]] = elt


def process_gen_nodes(app, doctree):
    # collect all gen_nodes in the environment
    # this is not gen_node in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    for elt in NODES:
        if not hasattr(env, NODES[elt]['env_all']):
            setattr(env, NODES[elt]['env_all'], [])

        for node in doctree.traverse(NODES[elt]['node_adm']):
            try:
                targetnode = node.parent[node.parent.index(node) - 1]
                if not isinstance(targetnode, nodes.target):
                    raise IndexError
            except IndexError:
                targetnode = None

            getattr(env, NODES[elt]['env_all']).append({
                'docname': env.docname,
                'source': node.source or env.doc2path(env.docname),
                'lineno': node.line,
                elt: node.deepcopy(),
                'target': targetnode,
            })


def process_gen_nodes_list(app, doctree, fromdocname):
    # Replace all gen_nodelist nodes with a list of the collected gen_nodes.
    # Augment each gen_node with a backlink to the original location.
    env = app.builder.env

    for elt in NODES:
        if not NODES[elt]['show_list']:
            for node in doctree.traverse(NODES[elt]['node_gen']):
                node.parent.remove(node)

        if not hasattr(env, NODES[elt]['env_all']):
            setattr(env, NODES[elt]['env_all'], [])

        for node in doctree.traverse(NODES[elt]['node_gen']):
            if not NODES[elt]['show_list']:
                node.replace_self([])
                continue

            content = []

            for gen_node_info in getattr(env, NODES[elt]['env_all']):

                if NODES[elt]['group_title_doc']:
                    if gen_node_info['target']['refid'] == 'index-0':
                        group = None
                        group = nodes.subtitle(classes=['%s-group' % elt])
                        group += nodes.Text(gen_node_info['docname'])
                        content.append(group)

                #para_desc
                para_desc = nodes.paragraph(classes=['%s-source' % elt])
                description = _('(The <<original entry>> is located in '
                                ' %s, line %d.)') % \
                              (gen_node_info['source'], gen_node_info['lineno'])
                desc1 = description[:description.find('<<')]
                desc2 = description[description.find('>>') + 2:]
                para_desc += nodes.Text(desc1, desc1)

                # Create a reference
                newnode = nodes.reference('', '', internal=True)
                innernode = nodes.emphasis(_(elt),
                                           _(elt))
                try:
                    newnode['refuri'] = app.builder.get_relative_uri(
                        fromdocname, gen_node_info['docname'])
                    newnode['refuri'] += '#' + gen_node_info['target']['refid']
                except NoUri:
                    # ignore if no URI can be determined, e.g. for LaTeX output
                    pass
                newnode.append(innernode)

                para_desc += newnode
                para_desc += nodes.Text(desc2, desc2)

                # (Recursively) resolve references in the gen_node content
                gen_node_entry = gen_node_info[elt]
                env.resolve_references(gen_node_entry,
                                       gen_node_info['docname'],
                                       app.builder)

                # Insert into the gen_nodelist
                gen_node_info[elt].children[0].children[0]=newnode
                content.append(gen_node_entry)
                if NODES[elt]['show_desc_paragraph']:
                    content.append(para_desc)

            node.replace_self(content)


def purge_gen_nodes(app, env, docname):

    for elt in NODES:
        if hasattr(env, NODES[elt]['env_all']):
            availables = [xgen_node for xgen_node in getattr(env, NODES[elt]['env_all'])
                          if xgen_node['docname'] != docname]
            setattr(env, NODES[elt]['env_all'], availables)


def visit_node(self, node):
    self.visit_admonition(node)


def depart_node(self, node):
    self.depart_admonition(node)


def setup(app):

# A NODES['elt']
#{'delayed': {'env_all': 'delayed_all_gen_nodes',
#             'meta_dir': <class 'sphinxcontrib.gen_node.Delayed'>,
#             'meta_dirlist': <class 'sphinxcontrib.gen_node.DelayedList'>,
#             'name': 'Delayed',
#             'namelist': 'DelayedList',
#             'node_adm': <class 'sphinxcontrib.gen_node.delayed'>,
#             'node_gen': <class 'sphinxcontrib.gen_node.delayedlist'>,
#             'show_list': True},

    setup_nodes(app.config._raw_config.get('gen_nodes', []))

    for elt in NODES:
        app.add_node(NODES[elt]['node_gen'])
        app.add_node(NODES[elt]['node_adm'],
                     html=(visit_node, depart_node),
                     latex=(visit_node, depart_node),
                     text=(visit_node, depart_node),
                     man=(visit_node, depart_node),
                     texinfo=(visit_node, depart_node))
        app.add_directive(elt, NODES[elt]['meta_dir'])
        app.add_directive(elt+LISTED, NODES[elt]['meta_dirlist'])

    app.connect('doctree-read', process_gen_nodes)
    app.connect('doctree-resolved', process_gen_nodes_list)
    app.connect('env-purge-doc', purge_gen_nodes)
