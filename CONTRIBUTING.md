# Contributing to OmniGlyph

Thank you for your interest in contributing to OmniGlyph.

Whether you are fixing bugs, improving documentation, adding features, or reporting issues, your contributions are appreciated.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/pshycodr/omniglyph.git
cd omniglyph
```

### Install Dependencies

OmniGlyph uses `uv` for dependency management.

```bash
uv sync
```

### Run the Application

```bash
uv run glyph/main.py
```

## Development Setup

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Build the standalone binary:

```bash
./scripts/build.sh
```

## Reporting Bugs

Before opening a bug report:

* Ensure you are using the latest version.
* Check existing issues to avoid duplicates.
* Include steps to reproduce the problem.
* Include screenshots when applicable.
* Include system information:

  * Linux distribution
  * Desktop environment
  * GTK version
  * Python version

A good bug report should clearly explain:

* What happened
* What you expected to happen
* How to reproduce the issue

## Suggesting Features

Feature requests are welcome.

When opening a feature request, include:

* The problem being solved
* The proposed solution
* Alternative solutions considered
* Any relevant screenshots or examples

## Pull Requests

### Before Submitting

Make sure:

* The application runs correctly.
* Existing functionality is not broken.
* Code is formatted.
* Changes are focused and easy to review.

### Commit Messages

Use clear and descriptive commit messages.

Examples:

```text
feat: add fuzzy emoji search
fix: resolve clipboard copy issue
docs: update installation instructions
refactor: simplify category filtering
```

## Code Style

General guidelines:

* Follow existing project conventions.
* Prefer readable code over clever code.
* Keep functions focused and small.
* Avoid unnecessary dependencies.
* Write descriptive variable and function names.

Format code with:

```bash
ruff format .
```

Lint code with:

```bash
ruff check .
```

## Project Structure

```text
glyph/
├── db/
│   ├── collections/
│   └── loader.py
├── ui/
│   ├── char_view.py
│   ├── search_bar.py
│   └── ...
├── main.py
└── ...
```

## Documentation

Documentation improvements are always welcome.

Examples:

* README improvements
* Installation guides
* Developer documentation
* Code comments
* Examples and screenshots

## License

By contributing to OmniGlyph, you agree that your contributions will be licensed under the **GNU General Public License v3.0** only.

See the [LICENSE](LICENSE) file for details.

## Questions

If you have questions, open a GitHub issue and provide as much detail as possible.

Thank you for helping improve OmniGlyph.
