import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

import ice

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'Ice'
copyright = '2014-{}, {}'.format(time.strftime('%Y'), ice.__author__)
author = ice.__author__
version = '.'.join(ice.__version__.split('.')[:2])
release = ice.__version__

language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_static_path = ['_static']


htmlhelp_basename = 'Icedoc'
latex_elements = {
}

latex_documents = [
  (master_doc, 'Ice.tex', 'Ice Documentation',
   'Susam Pal', 'manual'),
]

man_pages = [
    (master_doc, 'ice', 'Ice Documentation',
     [author], 1)
]

texinfo_documents = [
  (master_doc, 'Ice', 'Ice Documentation',
   author, 'Ice', 'One line description of project.',
   'Miscellaneous'),
]
