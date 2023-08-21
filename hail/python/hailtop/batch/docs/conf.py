# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import inspect
import datetime

# -- Project information -----------------------------------------------------

project = 'Batch'
copyright = '{}, Hail Team'.format(datetime.datetime.now().year)
author = 'Hail Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''
nitpicky = True
nitpick_ignore = [('py:class', 'hailtop.batch_client.client.Batch')]

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.5.4'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'IPython.sphinxext.ipython_console_highlighting',
    'sphinx_rtd_theme',
]

automodapi_inheritance_diagram = False

numpydoc_show_class_members = False

autosummary_generate = ['api.rst']
autosummary_generate_overwrite = True

napoleon_use_rtype = False
napoleon_use_param = True
# napoleon_include_private_with_doc = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates', '_templates/_autosummary']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {'python': ('https://docs.python.org/3.9', None)}


# -- Extension configuration -------------------------------------------------

def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


def has_docstring(obj):
    if inspect.ismethod(obj) or inspect.isfunction(obj):
        doc = obj.__doc__
        return doc is not None and len(doc) != 0
    return False


def autodoc_skip_member(app, what, name, obj, skip, options):
    exclusions = ('__delattr__', '__dict__', '__dir__', '__doc__', '__format__',
                  '__getattribute__', '__hash__', '__init__',
                  '__init_subclass__', '__new__', '__reduce__', '__reduce_ex__',
                  '__repr__', '__setattr__', '__sizeof__', '__str__',
                  '__subclasshook__', '__weakref__', 'maketrans')

    excluded_classes = ('str',)

    cls = get_class_that_defined_method(obj)

    exclude = (name in exclusions
               or (name.startswith('_') and not has_docstring(obj))
               or (cls and cls.__name__ in excluded_classes))

    return exclude


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.setup_extension('sphinx.ext.napoleon')
