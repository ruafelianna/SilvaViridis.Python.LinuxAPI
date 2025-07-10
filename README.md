![Github Actions](https://github.com/ruafelianna/SilvaViridis.Python.TemplateProject/workflows/Build/badge.svg)

# SilvaViridis.Python.TemplateProject

Template python project

### Usage

```python
"It will be here one day."
```

### Setup the Project

1. Install [Python](https://www.python.org/downloads/) and  [PDM](https://pdm-project.org/en/latest/#installation)

2. Execute in your shell

```sh
git clone git@github.com:ruafelianna/SilvaViridis.Python.TemplateProject.git \
    && cd SilvaViridis.Python.TemplateProject \
    && chmod u+x scripts/*.sh \
    && ./scripts/setup.sh
```

### Shell Scripts

- `./scripts/clean.sh` - cleans virtual environment and PDM Python version files.
- `./scripts/setup.sh` - does a clean installation of the development environment for this package and runs package build.
- `./scripts/update-gitignore.sh` - downloads fresh versions of Python, VS and VSCode `.gitignore` files and compiles them into one file. The old `.gitignore` file is removed. `curl` is required for this script to work.

### PDM Scripts

- `pdm run clean` - cleans build and test files.
- `pdm run build` - installs dependencies, runs static type checker and tests, builds a package.
- `pdm run test` - runs tests with coverage report.
- `pdm run update_lock` - updates `pdm.lock` file.

### Documentation

| Language | Link |
|:---:|:---:|
| English | [here](docs/en/index.md) |
