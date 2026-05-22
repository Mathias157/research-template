project = "Research Template"
author = "Mathias Berg Rosendal"
release = "0.1.0"

extensions = ["myst_parser"]
templates_path = ["_templates"]
exclude_patterns = ["build", "superpowers", "Thumbs.db", ".DS_Store", ".vault-mirror"]

html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]

# Markdown support
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
