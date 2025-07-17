# package-badges

This is a [deterministic](https://docs.automa.app/bots/types#deterministic) & [scheduled](https://docs.automa.app/bots/types#scheduled) [bot](https://docs.automa.app/bots/types#bot) for [**Automa**](https://automa.app) that automatically adds registry badges ([NPM](https://npmjs.org), [PyPI](https://pypi.org), [Cargo](https://crates.io)) to the README files of public packages.

#### Features

- Multiple registry badges:
  - **NPM**: version, license, and monthly downloads badges
  - **PyPI**: version, license, and monthly downloads badges
  - **Cargo**: version, license, and docs.rs documentation badges
- Support for monorepos with nested packages.
- Preserve existing README content, headings & badges.
- Handle both Markdown (`README.md`) and reStructuredText (`README.rst`).

## Getting Started

[![Install on Automa](https://automa.app/install.svg)](https://console.automa.app/$/bots/new/badges/package-badges)

### Self-Hosting

This bot can be self-hosted. You can follow these steps to get it running.

#### Prerequisites

- Have [`git`](https://git-scm.com/) installed.
- Have [`uv`](https://docs.astral.sh/uv/) installed.

#### Automa bot

[Create a bot](https://docs.automa.app/bot-development/create-bot) of [scheduled](https://docs.automa.app/bots/types#scheduled) type on [Automa](https://automa.app) (Cloud or Self-hosted) and point its webhook to your planned server (e.g., `http://your-server-ip:8000/hooks/automa`). Copy the **webhook secret** after it is created.

#### Starting the server

```sh
# Setup environment variables
export PYTHON_ENV=production
export AUTOMA_WEBHOOK_SECRET=your_secret_here

# Install dependencies
uv sync --frozen --no-dev

# Start server
uv run fastapi run --port 8000
```

## How It Works

The bot scans your repository for package manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`). For each public package it finds, it generates a set of badges and inserts them into the corresponding `README.md` or `README.rst` file.

#### Private Package Detection

The bot automatically skips private packages by checking:

- **NPM**: `private` field set to `true` in `package.json`.
- **PyPI**: The presence of a `Private ::` classifier in `pyproject.toml`.
- **Cargo**: `publish` field set to `false` or a list that does not include `crates-io` in `Cargo.toml`.

## Contributing

Contributions and feedback are welcome! Feel free to open an issue or submit a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details. Here is a list of [Contributors](https://github.com/automa/package-badges/contributors).

## LICENSE

MIT

## Bug Reports

Report [here](https://github.com/automa/package-badges/issues).
