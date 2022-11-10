# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Medisee"
copyright = "2022, Medisee"
author = "Medisee"
release = "1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = "README"

root_url = "../../"
html_context = {
    "root_url": root_url,
}
templates_path = ["_templates"]

extensions = [
    "sphinx.ext.intersphinx",
    "myst_parser",
    ]

intersphinx_mapping = {
  "backend": (root_url + "medctrl-backend/API/docs/html", None),
  }

include_patterns = [
    "index.rst",
    "README.md",
]

exclude_patterns = [
    "**/venv",
    "**/__pychache__",
    "**/node_modules",
    ]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_logo = "_static/medisee.svg"
html_theme_options = {
    "logo_only": True,
    "collapse_navigation": False,
    "navigation_depth": -1,
    "sticky_navigation": False,
}
html_copy_source = False
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
