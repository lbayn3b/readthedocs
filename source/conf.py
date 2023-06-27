# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Ajax Deployment'
copyright = '2021, N3bula Systems'
author = 'N3bula Systems'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [ 'sphinx.ext.napoleon', 'sphinx_rtd_theme', 'sphinx.ext.todo', 'sphinx.ext.autosectionlabel'
                ]

pdf_documents = [('index', u'N3bula Systems Docs', u'N3bula Systems Docs', u'N3bula Systems')]

todo_include_todos : True  

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_logo = 'transparent_logo.png'

html_theme_options = {
        'collapse_navigation' : False,
        "prev_next_buttons_location" : "both",
        "logo_only" : True,
        "display_version" : False,
        'navigation_depth': -1,
        'show_sphinx': False,
        'theme_prev_next_buttons_location': 'both',
        'extrafooter': 'N3bula Systems Inc',
        }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
latex_elements = {
        'figure_align':'H'
}
html_static_path = [ '_static' ]

html_css_files = [
        'custom.css'
]