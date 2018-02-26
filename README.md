# `github-app-demo.py`

A _Pythonic_ way of developing [GitHub Apps](https://developer.github.com/apps/).

## Examples

```python
from github import App
app = App()

# Get a specific installation of this App
installation = app.get_installation('octocat')

# Get all the repositories associated with installation
repositories = installation.get_repositories()

# :soon:
repository = app.get_repository('octocat/Hello-World')
```

More :soon:

## Get started

:construction: `TODO` :construction:
