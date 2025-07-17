# How to Contribute

## Prerequisites

- Have [`git`](https://git-scm.com/) installed.
- Have [`uv`](https://docs.astral.sh/uv/) installed.
- Have a [scheduled](https://docs.automa.app/bots/types#scheduled) bot in either [Automa](https://automa.app) (Cloud or Self-hosted) or in [automa/monorepo](https://github.com/automa/monorepo) local setup.

## Setup environment variables

```sh
export AUTOMA_WEBHOOK_SECRET=your_secret_here
```

## Installing dependencies

```sh
uv sync
```

## Starting the server

```sh
uv run fastapi dev --port=5005
```

## CI/CD

#### Testing

```sh
export PYTHON_ENV=test
uv run pytest
```

#### Linting

```sh
uv run ruff check
```

#### Formatting

```sh
uv run ruff format
```
