# GitItPyTest

This repository in used by the Git-It utility.  The ``push`` test must connect
to anonline

## Dependencies

- Python 3.10
- FastAPI
- uvicorn
- Docker

## Running Locally

There are two approaches to running the API locally.

**Run the API directly**

```
> python3.10 -m venv .venv
> source .venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
> ./run.sh
```

**Run the API via Docker Compose**

Make sure the environment variables are set in the current environment.

```bash
export PROJECT_ID=$(gcloud config get-value project)
export GCP_KEY_PATH=[path to the service account credential file]
```
Project Short Description (default ini)

    Project long description or extended summary goes in here (default ini)

=======
Testing
=======

This project uses ``pytest`` to run tests and also to test docstring examples.

Install the test dependencies.

.. code-block:: bash

    $ pip install -r requirements_test.txt

Run the tests.

==========
Developing
==========

This project uses ``black`` to format code and ``flake8`` for linting. We also support ``pre-commit`` to ensure these have been run. To configure your local environment please install these development dependencies and set up the commit hooks.

.. code-block:: bash

    $ pip install black flake8 pre-commit
    $ pre-commit install

=========
Releasing
=========

Releases are published automatically when a tag is pushed to GitHub.

.. code-block:: bash

    # Set next version number
    export RELEASE = x.x.x

    # Create tags
    git commit --allow -empty -m "Release $RELEASE"
    git tag -a $RELEASE -m "Version $RELEASE"

    # Push
    git push upstream --tags
