=======================
sphinxcontrib-gen_node
=======================

A generic "todo like" nodes.

You love sphinx-ext-todo, and want more directives like this ?

This extension is for you.

`install me`_ with zc.buildout or clone and setup.py install|develop and add this to your conf.py ::
 
 extensions = ['sphinxcontrib.gen_node'] 
 gen_nodes = [('sample_one', True), ('sample_two', True), ('sample_three', True)]


explanations 
=============

gen_nodes is a list of tuples which for each element you could now add in your documentation like you do with 'sphinx-ext-todo':

* a new sample_one directive
 ::

  .. sample_one::  one thing
 



* a new sample_onelist directive
 ::
  
   .. sample_onelist::

               

The  sample_onelist will not appear in your documentation if you set False in your conf.py   gen_nodes = [('sample_one', False),...

Plz note that  the form of a "list directive is always 'namenode'+list



_`install me`
=============

with buildout 

edit a buildout.cfg like this ::

 [buildout]

 extensions =
     mr.developer
     buildout-versions

 auto-checkout = sphinxcontrib-gen_node

 parts =
     sphinx

 [sphinx]                                   :
 recipe = zc.recipe.egg
 eggs =
     Sphinx
     sphinxcontrib-gen_node

 [sources]
 sphinxcontrib-gen_node = git git@github.com:jpcw/sphinxcontrib-gen_node.git

 [versions]

then play your buildout configuration ::

 wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
 python boostrap.py -d 

 bin/buildout -Nv

create your documentation::

 bin/sphinx-quickstart

edit your Makefile | make.bat like this ::

 SPHINXBUILD   = bin/sphinx-build

update your source/conf.py::

 extensions = ['sphinxcontrib.gen_node'] 
 gen_nodes = [('sample_one', True), ('sample_two', True), ('sample_three', True)]    


Enjoy

