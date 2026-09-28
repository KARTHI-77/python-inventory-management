# Week 6 – Continuous Integration (CI) Documentation

## 1. Project Overview

This project is a Python-based Inventory Management module with automated unit and integration tests. The Week 6 task integrates Continuous Integration (CI) into the existing project using GitHub Actions.

The purpose of the CI pipeline is to automatically check code quality and run the project's automated tests whenever the configured repository events occur.

## 2. CI Tool Used

The project uses **GitHub Actions** as its Continuous Integration tool.

The workflow file is located at:

```text
.github/workflows/tests.yml
```

The workflow runs on pushes to the configured branches and on pull requests targeting the `main` branch.

## 3. CI Pipeline Configuration

The GitHub Actions workflow performs the following stages:

1. Checks out the repository.
2. Sets up Python 3.14.
3. Installs the project dependencies.
4. Installs Flake8 for code linting.
5. Runs Flake8 against the `inventory` and `tests` directories.
6. Runs the complete pytest test suite.
7. Runs pytest with coverage reporting.

The workflow is configured so that a command returning a failure status causes the GitHub Actions job to fail.

## 4. Code Linting

Flake8 was integrated into the CI workflow to check Python code style and detect common code-quality issues.

The local linting command is:

```powershell
python -m flake8 inventory tests
```

The project was cleaned up to resolve the reported formatting issues. The final local Flake8 run completed without any reported errors.

## 5. Automated Testing

The project uses pytest for automated testing.

The local test command is:

```powershell
pytest -v
```

The final verification collected **37 tests**, and all **37 tests passed**.

The test suite includes unit tests for the inventory manager and integration tests for inventory file operations.

## 6. Test Coverage

Coverage is generated using pytest-cov.

The local command is:

```powershell
pytest --cov=inventory --cov-report=term-missing
```

The final verification reported:

```text
inventory\__init__.py    100%
inventory\manager.py    100%
TOTAL                   100%
```

The final run completed with **37 passed tests** and **100% total coverage**.

## 7. Running the Project Checks Locally

Activate the project's virtual environment and run:

```powershell
python -m flake8 inventory tests
pytest -v
pytest --cov=inventory --cov-report=term-missing
```

These commands reproduce the main quality checks performed by the CI workflow.

## 8. Viewing CI Results

After pushing a change to a configured branch or creating/updating a pull request targeting `main`, GitHub Actions runs the workflow.

The workflow results can be viewed from:

```text
GitHub repository → Actions → Python Tests
```

The successful Week 6 CI run showed green checks for:

- Checkout repository
- Set up Python
- Install dependencies
- Run linting
- Run tests
- Run tests with coverage

## 9. Challenges and Resolutions

During the local setup, Flake8 was initially installed in the global Python environment but was not available inside the project's `.venv`. Installing Flake8 inside the virtual environment resolved this issue.

The initial linting run also identified formatting issues such as incorrect indentation, whitespace on blank lines, missing final newlines, and insufficient blank lines between test functions. These issues were corrected and the project was rechecked successfully.

## 10. Final Verification

The final local verification produced:

```text
Python: 3.14.7
Pytest: 9.1.1
Tests: 37 passed
Coverage: 100%
Flake8: passed
```

The GitHub Actions CI workflow also completed successfully with all configured pipeline stages passing.

## 11. Conclusion

The inventory management project now has an automated CI workflow using GitHub Actions. The pipeline combines linting, automated testing, and coverage reporting so that code changes can be checked consistently. The successful local and GitHub Actions verification demonstrates that the CI configuration is integrated with the existing Python test suite.
