# Contributing to User Research AI Agents

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest tests/`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for your changes
4. Ensure all tests pass: `pytest tests/`
5. Format code: `black . && ruff check .`
6. Commit your changes
7. Push to your fork
8. Open a Pull Request

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use Ruff for linting
- Write type hints where possible
- Add docstrings for public functions

## Testing

- All new features should include tests
- Run tests with: `pytest tests/ -v`
- Aim for >80% code coverage

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (add, fix, update, remove)
- Keep the first line under 72 characters
- Add body for detailed explanation if needed

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Update CHANGELOG.md if applicable
4. Request review from a maintainer
5. Once approved,Squash and merge

## Questions?

Feel free to open an issue for questions or discussions.
