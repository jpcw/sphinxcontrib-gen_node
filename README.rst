=======================
sphinxcontrib-gen_node
=======================

A generic "todo like" nodes.

You love sphinx-ext-todo, and want more directives like this ?

This extension is for you.


`install me`_ with zc.buildout| pip | easy_install or clone and setup.py install|develop and add this to your conf.py ::
 
 extensions = ['sphinxcontrib.gen_node'] 
 gen_nodes = [('sample_one', True, True, False), ('sample_two', True, False, False),]


explanations 
=============

gen_nodes is a list of tuples which for each element you could now add in your documentation like you do with 'sphinx-ext-todo':

* a new sample_one directive ::

  .. sample_one::  one thing
 



* a new sample_onelist directive ::
  
   .. sample_onelist::

               

The  sample_onelist will not appear in your documentation if you set False in your conf.py   gen_nodes = [('sample_one', False, False, False),... on the second argument.

options :

 + sample_one is the name of your new admonition, you'll write ::

   .. sample_one:: A text here

 + The first (True|False) argument enables the list Plz note that  the form of a "list directive is always 'namenode'+list ie ::

   .. sample_onelist:: 

 + the second (True|False) renders gathering by doc subtitle 

 + the third (True|False) renders a paragraph with filename and line number (like on todo-list) with sphinxext.todo 



_`install me`
=============

easy_install ::
 
 easy_install sphinxcontrib-gen_node
 

pip ::
 
 pip install Sphinx
 pip sphinxcontrib-gen_node

zc.buildout ::

 eggs =
     Sphinx
     sphinxcontrib-gen_node


update your source/conf.py::

 extensions = ['sphinxcontrib.gen_node'] 
 gen_nodes = [('sample_one', True, True, False), ('sample_two', True, False, False)]    


Credits
========
Companies
---------
|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.com>`_
      * `Contact us <mailto:python@makina-corpus.org>`_

      .. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
      .. _makinacom:  http://www.makina-corpus.com


