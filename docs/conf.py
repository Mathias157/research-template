project = 'Research Template'
author = 'Mathias Berg Rosendal, Théodore Le Nalinec'
release = '0.1.0'

extensions = ['myst_parser']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.vault-mirror']

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# Markdown support
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
