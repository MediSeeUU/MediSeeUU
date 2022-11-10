# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django
sys.path.insert(0, os.path.abspath("../../"))
if os.getenv("GITHUB_ACTION"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "api_settings.settings.common"
else:
    os.environ["DJANGO_SETTINGS_MODULE"] = "api_settings.settings.dev_settings"

django.setup()
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Backend"
copyright = "2022, Medisee"
author = "Medisee"
release = "1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ["_templates"]

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    ]

autosummary_generate = True

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
html_static_path = ["../../../../docs/sphinx-source/_static"]
html_logo = html_static_path[0] + "/medisee.svg"
html_theme_options = {
    "logo_only": True,
    "collapse_navigation": False,
    "navigation_depth": -1,
    "sticky_navigation": False,
}
html_show_sourcelink = False
html_css_files = ["css/custom.css"]
