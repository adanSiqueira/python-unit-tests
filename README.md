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

A practical, structured learning repository to master **Python unit testing with pytest** module.

This repo walks you step by step — from simple functions to mocking APIs and testing Flask endpoints — showing **how** and **why** each testing concept works.

It contains the **examples and cases proposed in the tutorial "Please Learn How To Write Tests in Python… • Pytest Tutorial"** on [Tech With Tim](https://www.youtube.com/watch?v=EgpLj86ZHFQ), demonstrating practical usage of **pytest**, **mocking functions and classes**, and **Flask API testing**.


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

| Folder | Topic | Key Concepts |
|---------|--------|--------------|
| `1-simple-functions-example/` | Basic unit testing | Assertions, test discovery |
| `2-fixtures-setup-example/` | Fixtures (setup) | `@pytest.fixture`, reusable setups |
| `3-fixtures-teardown/` | Setup & teardown | Yield fixtures, cleanup steps |
| `4-parametrized-testing/` | Parametrized tests | `@pytest.mark.parametrize` |
| `5-mocking/` | Mocking | `mocker` fixture, patching, fakes |
| `6-example-testing-an-api/` | API testing | Flask test client, HTTP assertions |

---


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

---
##  Author

**Adan Siqueira**  
🔗 [GitHub Profile](https://github.com/AdanSiqueira)

---

If you like this project, don’t forget to ⭐ **star the repository** to show your support!
