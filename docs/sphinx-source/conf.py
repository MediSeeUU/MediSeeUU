# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Medisee'
copyright = '2022, Medisee'
author = 'Medisee'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = 'README'

extensions = [
    'sphinx.ext.intersphinx',
    'myst_parser',
    ]

intersphinx_mapping = {
  'backend': ('../../medctrl-backend/API/docs/html', None),
  }

include_patterns = [
    'index.rst',
    'README.md',
]

exclude_patterns = [
    '**/venv',
    '**/__pychache__',
    '**/node_modules',
    ]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': -1,
    'sticky_navigation': False,
}
html_show_sourcelink = False
