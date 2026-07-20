# Contributing to pakdocling

Thanks for your interest in contributing to pakdocling.

## Ways to Contribute

- Opening issues
- Improving documentation
- Fixing bugs
- Adding features
- Creating test fixtures
- Improving benchmarks
- Reviewing pull requests

## Before You Start

- Search existing issues before opening a new one
- Keep discussions constructive
- Open an issue before working on major changes

## Development Setup

Requires Python 3.10+.

```bash
git clone https://github.com/YOUR_USERNAME/pakdocling.git
cd pakdocling
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development Workflow

```bash
git checkout -b feature/my-feature
# Make changes
git commit -m "Add feature X"
git push origin feature/my-feature
# Open a Pull Request
```

## Pull Request Guidelines

- Be focused and small when possible
- Include clear descriptions
- Reference related issues
- Pass tests and checks
- Avoid unrelated refactors

## Coding Standards

- Write readable and modular code
- Use type hints where useful
- Keep dependencies minimal
- Follow PEP 8
- Use virtual environments

## Reporting Bugs

Include:

- Expected behavior
- Actual behavior
- Reproduction steps
- Environment details

## Security

Do not publicly disclose security vulnerabilities. Report them privately to the maintainers.

## Community

Be respectful and collaborative.

## License

By contributing, you agree that your contributions will be licensed under the repository license.
