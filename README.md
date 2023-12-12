# Docker-blueprint
[![GitHub Actions][github-actions-badge]](https://https://github.com/OpenConsultingUK/docker-blueprint/actions)
[![Poetry][poetry-badge]](https://python-poetry.org/)
[![Nox][nox-badge]](https://github.com/wntrblm/nox)
[![Ruff][ruff-badge]](https://github.com/astral-sh/ruff)

[github-actions-badge]: https://github.com/OpenConsultingUK/docker-blueprint/workflows/python/badge.svg
[poetry-badge]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
[nox-badge]: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json

Example docker project that demonstrates how to create a Python package using the latest
Python testing, linting, and type checking tooling. The project contains a `fact` package that
provides a simple implementation of the [factorial algorithm](https://en.wikipedia.org/wiki/Factorial) (`fact.lib`).
# Requirements

Python 3.10

# Package Management

This package uses [Poetry](https://python-poetry.org/) to manage dependencies and
isolated [Python virtual environments](https://docs.python.org/3/library/venv.html).

To proceed,
[install Poetry globally](https://python-poetry.org/docs/#installation)
onto your system.

## Dependencies

Dependencies are defined in [`pyproject.toml`](./pyproject.toml) and specific versions are locked
into [`poetry.lock`](./poetry.lock). This allows for exact reproducible environments across
all machines that use the project, both during development and in production.

To install all dependencies into an isolated virtual environment:

> Append `--sync` to uninstall dependencies that are no longer in use from the virtual environment.

```bash
poetry install
```

To [activate](https://python-poetry.org/docs/basic-usage#activating-the-virtual-environment) the
virtual environment that is automatically created by Poetry:

```bash
poetry shell
```

To deactivate the environment:

```bash
(fact-py3.10) $ exit
```

To upgrade all dependencies to their latest versions:

```bash
$ poetry update
```

# Enforcing Code Quality

Automated code quality checks are performed using 
[Nox](https://nox.thea.codes/en/stable/) and
[`nox-poetry`](https://nox-poetry.readthedocs.io/en/stable/). Nox will automatically create virtual
environments and run commands based on [`noxfile.py`](./noxfile.py) for unit testing, PEP 8 style
guide checking, type checking and documentation generation.

> Note: `nox` is installed into the virtual environment automatically by the `poetry install`
> command above. Run `poetry shell` to activate the virtual environment.

To run all default sessions:

```bash
(fact-py3.10) $ nox
```

## Unit Testing

Unit testing is performed with [pytest](https://pytest.org/). pytest has become the de facto Python
unit testing framework. Some key advantages over the built-in
[unittest](https://docs.python.org/3/library/unittest.html) module are:

1. Significantly less boilerplate needed for tests.
2. PEP 8 compliant names (e.g. `pytest.raises()` instead of `self.assertRaises()`).
3. Vibrant ecosystem of plugins.

pytest will automatically discover and run tests by recursively searching for folders and `.py`
files prefixed with `test` for any functions prefixed by `test`.

The `tests` folder is created as a Python package (i.e. there is an `__init__.py` file within it)
because this helps `pytest` uniquely namespace the test files. Without this, two test files cannot
be named the same, even if they are in different subdirectories.

Code coverage is provided by the [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin.

When running a unit test Nox session (e.g. `nox -s test`), an HTML report is generated in
the `htmlcov` folder showing each source file and which lines were executed during unit testing.
Open `htmlcov/index.html` in a web browser to view the report. Code coverage reports help identify
areas of the project that are currently not tested.

pytest and code coverage are configured in [`pyproject.toml`](./pyproject.toml).

To pass arguments to `pytest` through `nox`:

```bash
(fact-py3.10) $ nox -s test -- -k invalid_factorial
```

## Code Style Checking

[PEP 8](https://peps.python.org/pep-0008/) is the universally accepted style guide for Python
code. PEP 8 code compliance is verified using [Ruff][Ruff]. Ruff is configured in the
`[tool.ruff]` section of [`pyproject.toml`](./pyproject.toml).

[Ruff]: https://github.com/astral-sh/ruff

Some code style settings are included in [`.editorconfig`](./.editorconfig) and will be configured
automatically in editors such as PyCharm.

To lint code, run:

```bash
(fact-py3.10) $ nox -s lint
```

To automatically fix fixable lint errors, run:

```bash
(fact-py3.10) $ nox -s lint_fix
```

## Automated Code Formatting

[Ruff][Ruff] is used to automatically format code and group and sort imports.

To automatically format code, run:

```bash
(fact-py3.10) $ nox -s fmt
```

## Type Checking
[Type annotations](https://docs.python.org/3/library/typing.html) allows developers to include
optional static typing information to Python source code. This allows static analyzers such
as [mypy](http://mypy-lang.org/), [PyCharm](https://www.jetbrains.com/pycharm/),
or [Pyright](https://github.com/microsoft/pyright) to check that functions are used with the
correct types before runtime.

Editors such as [PyCharm](https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html) and
VS Code are able to provide much richer auto-completion, refactoring, and type checking while the
user types, resulting in increased productivity and correctness.

```python
def factorial(n: int) -> int:
    ...
```

mypy is configured in [`pyproject.toml`](./pyproject.toml). To type check code, run:

```bash
(fact-py3.10) $ nox -s type_check
```

See also [awesome-python-typing](https://github.com/typeddjango/awesome-python-typing).

# Project Structure

Traditionally, Python projects place the source for their packages in the root of the project
structure, like:

``` {.sourceCode .}
factorial
├── src
│     └── fact
|           ├── __init__.py
│           └── lib.py
├── tests
│     └── init.py
├── views
│     └── fast_api
│           ├── fastapi_app.py
│           └── api.dockerfile
|     ├── flask
│           └── static
|                  └── style.css
│           └── templates
│                  └── index.html
│           └── app.py
│           └── web.dockerfile
|     ├── nginx
│          ├── certs # Add SSL Certificate and Key
|          ├── default.conf
│          ├── get_cert.sh
│          └── nginx.dockerfile
├── docker-compose.yml
├── noxfile.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── .dockerignore
└── .gitignore

# Add SSL Certificate and Key for domain(s)
Refer: [Link to Another README](views/nginx/certs/README.md)

# Container

[Docker](https://www.docker.com/) is a tool that allows for software to be packaged into isolated
containers. It is not necessary to use Docker in a Python project, but for the purposes of
presenting best practice examples, a Docker configuration is provided in this project. The Docker
configuration in this repository is optimized for small size and increased security, rather than
simplicity.

Docker is configured in:

- [`Dockerfile`](./Dockerfile)
- [`.dockerignore`](./.dockerignore)

To build the container image:

```bash
/docker-blueprint$ docker build --no-cache --tag image -f  dockerfile_path .
```

To run the image in a container:

```bash
/docker-blueprint$ docker run --rm -it image /bin/bash
```

To publish a container's port(s) to the host machine
```bash
/docker-blueprint$ docker run -p host_port:container_port image

```
# Docker-compose
The documentation can be found [here](https://pdmlab.github.io/docker-compose/).

To Build and Start the Application
```bash
docker-compose up --remove-orphans
```
To stop the application and clean up resources
```bash
docker-compose down --remove-orphans
```
To further clean up resources: 
- To delete all containers including its volumes use,
```bash
docker rm -vf $(docker ps -aq)
```
- To delete all the images,
```bash
docker rmi -f $(docker images -aq)
```