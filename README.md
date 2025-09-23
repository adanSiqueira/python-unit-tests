<h1 align="center">Python Unit Testing</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue" alt="Python">
  <img src="https://img.shields.io/badge/Pytest-8.4.2-orange" alt="Pytest">
  <img src="https://img.shields.io/badge/Flask-2.3.2-red" alt="Flask">
  <img src="https://img.shields.io/badge/TDD-Study-green" alt="TDD">
</p>

---

## Repository Overview

This repository is a **study-focused collection** of examples, exercises, and theory on **Unit Testing and Automated Testing in Python**.  
It contains practical examples covering:

- Writing **unit tests** for functions and classes
- Using **pytest fixtures** for setup and teardown
- Mocking **functions** and **classes** with `mocker`
- Parametrized testing
- Testing **Flask API endpoints**
- Conceptual explanations of **unit tests, integration tests, system tests, and automated testing**
- Practical examples demonstrating **best practices** for Python testing

The goal of this repo is to serve as a **learning resource** for Python developers who want to deepen their understanding of testing, from basics to intermediate concepts.

---

## Repository Structure
```
api.py      -> Simulated Flask API for testing
test_api.py -> Tests for the Flask API

Python-Testing/
├── fixtures-setup-example/
│ ├── main.py   -> Example functions to be tested
│ └── test_main.py  -> Tests using setup fixtures
├── fixtures-teardown/
│ ├── db.py  -> Simulated database module
│ └── test_db.py -> Tests using teardown fixtures
├── mocks-classes/
│ ├── service.py -> Example class to be tested
│ └── test_service.py -> Tests mocking classes
├── mocks-functions/
│ ├── db.py -> Example function to be tested
│ ├── main.py -> Example functions to be tested
│ ├── test_db.py -> Tests mocking functions
│ └── test_main.py -> Tests for main.py
├── parametrized-testing/
│ ├── main.py -> Example parametrized functions to be tested
│ └── test_main.py -> Parametrized tests
├── theory/
│ ├── fixtures.pdf -> Explanation of pytest fixtures
│ ├── mocking.pdf -> Explanation of mocking in tests
│ ├── testing_types.pdf -> Overview of different test types
│ └── unit_testing.pdf -> General unit testing theory
└── simple-functions-example/
    ├── main.py -> Simple functions to be tested
    └── test_main.py -> Tests for simple functions
requirements.txt -> Project dependencies
README.md  -> This file
```


### Highlights

- **Fixtures**: setup and teardown examples for database and object lifecycle management.
- **Mocks**: clear comparison between mocking **functions** vs **classes**.
- **Parametrized Tests**: reducing repetition and testing multiple cases efficiently.
- **Flask API Testing**: demonstrating testing of endpoints with `client` fixtures.
- **Documentation**: PDFs explaining testing concepts, fixtures, mocking, and general theory.

---

## Getting Started

### Install Dependencies

```bash
pip install requirements.txt
```

### Run Tests

```bash
pytest
```
- All test files follow the pattern test_*.py.
- Use pytest --maxfail=1 --disable-warnings -q for concise output.

### Learning Goals

- Learn how to write clean unit tests for functions and classes.
- Understand how to use pytest fixtures for test setup and teardown.
- Learn when and how to mock functions vs classes.
- Learn best practices for parametrized testing to avoid repetition.
- Learn how to test APIs built with Flask.
- Understand the theory behind unit, integration, system, and end-to-end testing.
- Understand how automated tests fit into CI/CD pipelines.

### Tech Stack / Tools
Python 3.13
pytest 8.4.2
Flask 2.3.2
mocker (pytest-mock) 3.10.0