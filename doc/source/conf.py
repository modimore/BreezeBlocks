#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath('../../package'))
import breezeblocks

# -- General configuration ------------------------------------------------

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig']

templates_path = ['_templates']

source_suffix = ['.rst']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'BreezeBlocks'
copyright = '2017, Quinn Mortimer'
author = 'Quinn Mortimer'

# The short X.Y version.
version = breezeblocks.version
# The full version, including alpha/beta/rc tags.
release = breezeblocks.version

language = None

exclude_patterns = []

pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

autoclass_content = 'both'

# -- Options for HTML output ----------------------------------------------
html_theme = 'classic'
# html_theme_options = {}
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'BreezeBlocksdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'BreezeBlocks.tex', 'BreezeBlocks Documentation',
     'Quinn Mortimer', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'breezeblocks', 'BreezeBlocks Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'BreezeBlocks', 'BreezeBlocks Documentation',
     author, 'BreezeBlocks', 'One line description of project.',
     'Miscellaneous'),
]
