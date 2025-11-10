Here it is a **complete, well-structured theoretical and practical review** for understanding **mocking in tests**, especially in `pytest` — going from the core concept, to use cases, code examples, and advanced mocking patterns.

---

# Mocking in Testing (with Pytest)

Mocking is one of the most **important and powerful tools** in software testing. It allows you to **simulate external dependencies**, control their behavior, and **test your code in isolation**.

---

## 1. What is Mocking?

**Mocking** means creating **fake (mocked) versions of objects, functions, or APIs** so you can:

* Control their **return values** or **side effects**.
* Avoid hitting real APIs, databases, or file systems.
* Ensure your tests are **fast, deterministic, and isolated**.

Mocks are used to test **your logic**, not the dependencies’ behavior.

---

### Example: Why You Need Mocking

Imagine a function that calls a weather API:

```python
import requests

def get_weather(city):
    response = requests.get(f"https://weatherapi.com/{city}")
    data = response.json()
    return {"temp": data["temp"], "condition": data["condition"]}
```

If you test it *as is*, your test would:

* Depend on internet access.
* Fail if the API is down.
* Potentially cost you money or rate-limit your tests.

 **Solution**: Mock the `requests.get` call — simulate its behavior.

---

##  2. The `unittest.mock` Module

Python’s built-in [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html) module provides tools for creating mocks.

Key components:

* `Mock` and `MagicMock`: Create fake objects.
* `patch`: Temporarily replace objects or functions during a test.
* `patch.object`: Replace attributes on existing objects.
* `mock_open`: Simulate file operations.
* `side_effect`: Simulate exceptions or multiple returns.

Pytest integrates seamlessly with it — especially through the **`mocker` fixture** from `pytest-mock`.

---

## 3. Using `pytest-mock`

Install it first:

```bash
pip install pytest-mock
```

This provides a **`mocker` fixture**, which wraps `unittest.mock` utilities, making mocking simpler and more readable in pytest.

---

## 4. Example — Mocking an API Call

Let’s rewrite your note in a complete working example.

### app.py

```python
import requests

def get_weather(city):
    response = requests.get(f"https://weatherapi.com/{city}")
    if response.status_code != 200:
        raise ValueError("API error")
    return response.json()
```

### test_app.py

```python
def test_get_weather_success(mocker):
    # 1. Patch the requests.get function inside app module
    mock_get = mocker.patch("app.requests.get")

    # 2. Configure the mock
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "temp": 25,
        "condition": "Sunny"
    }

    # 3. Call function under test
    from app import get_weather
    result = get_weather("London")

    # 4. Assertions
    assert result == {"temp": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://weatherapi.com/London")
```

 **Explanation**

* `mocker.patch("app.requests.get")`: replaces `requests.get` **only inside your module** (`app`).
* The mock behaves like a normal object: you can set attributes like `.return_value` or `.json.return_value`.
* The original `requests.get` is restored after the test automatically.

---

## 5. Why Patch Inside Your Module (Not Globally)

When patching, you must **mock where the function is used, not where it’s defined**.

Bad (won’t work as intended):

```python
mocker.patch("requests.get")
```

Good:

```python
mocker.patch("app.requests.get")
```

That’s because Python modules keep their own *references* to imported functions — so your patch must target that reference.

---

## 6. Mock Return Values

You can control what your mocked object returns.

```python
mock_get.return_value.status_code = 200
mock_get.return_value.json.return_value = {"key": "value"}
```

You can also chain calls:

```python
mock_get().json()  # returns your specified value
```

This pattern mimics the way real objects are used.

---

## 7. Simulating Exceptions with `side_effect`

You can simulate **errors or multiple responses** using `side_effect`.

Example: simulate API failure

```python
mock_get.side_effect = Exception("Network error")

with pytest.raises(Exception):
    get_weather("Paris")
```

Example: simulate multiple responses

```python
mock_get.side_effect = [
    mocker.Mock(status_code=500),
    mocker.Mock(status_code=200, json=lambda: {"temp": 10}),
]
```

---

## 8. Mocking Classes and Methods

You can also mock class instantiation or methods.

### Example

```python
class PaymentGateway:
    def charge(self, amount):
        return {"status": "success", "id": 123}

def process_payment(amount):
    gateway = PaymentGateway()
    result = gateway.charge(amount)
    return result["status"]
```

### Test

```python
def test_process_payment(mocker):
    mock_gateway = mocker.patch("app.PaymentGateway")
    mock_gateway.return_value.charge.return_value = {"status": "success"}

    from app import process_payment
    status = process_payment(100)

    assert status == "success"
    mock_gateway.assert_called_once()
```

The entire class is replaced by a mock.
When `PaymentGateway()` is called, the mock intercepts it, and you control its behavior.

---

## 9. Mocking External Libraries or APIs

Example: mocking OpenAI or AWS SDKs.

```python
def summarize_text(api_client, text):
    return api_client.summarize(text)
```

Test:

```python
def test_summarize_text(mocker):
    mock_api = mocker.Mock()
    mock_api.summarize.return_value = "Short summary."

    from app import summarize_text
    result = summarize_text(mock_api, "long text...")
    assert result == "Short summary."
    mock_api.summarize.assert_called_once_with("long text...")
```

Here we didn’t even patch — we simply created a fake object with `.Mock()`.

---

## 10. Mocking File Operations (`mock_open`)

```python
from unittest.mock import mock_open

def read_file(path):
    with open(path) as f:
        return f.read()
```

Test:

```python
from unittest.mock import patch, mock_open

def test_read_file():
    m = mock_open(read_data="mocked content")
    with patch("builtins.open", m):
        from app import read_file
        assert read_file("file.txt") == "mocked content"
```

 No file is ever created — completely simulated I/O.

---

## 11. Mocking Time or Randomness

These are common targets for mocking to make tests deterministic.

```python
import time, random

def get_id():
    return f"{int(time.time())}-{random.randint(1,100)}"
```

Test:

```python
def test_get_id(mocker):
    mocker.patch("app.time.time", return_value=1000)
    mocker.patch("app.random.randint", return_value=42)

    from app import get_id
    assert get_id() == "1000-42"
```

---

## 12. Verifying Mock Behavior

Mocks record every interaction:

* `assert_called()`
* `assert_called_once()`
* `assert_called_with(args)`
* `assert_any_call(args)`
* `call_args_list` (list of all calls)

Example:

```python
mock_get.assert_called_once_with("https://weatherapi.com/London")
assert mock_get.call_count == 1
```

---

## 13. Mock vs Stub vs Spy (Conceptually)

| Term     | Description                              | Example                          |
| -------- | ---------------------------------------- | -------------------------------- |
| **Mock** | Fake object that records how it’s used   | `mock_get.assert_called_once()`  |
| **Stub** | Simplified object returning fixed values | `mock_get.return_value = {...}`  |
| **Spy**  | Wraps a real object, tracking calls      | `mocker.spy(real_obj, "method")` |

Example spy:

```python
def test_spy_example(mocker):
    class Calculator:
        def add(self, a, b): return a + b

    calc = Calculator()
    spy = mocker.spy(calc, "add")

    result = calc.add(1, 2)
    spy.assert_called_once_with(1, 2)
    assert result == 3
```

---

## 14. Mocking Asynchronous Functions

For async functions, you can mock using `AsyncMock` (Python 3.8+):

```python
from unittest.mock import AsyncMock

async def fetch_data():
    return {"data": 123}
```

Test:

```python
def test_async_fetch(mocker):
    mocker.patch("app.fetch_data", new_callable=AsyncMock, return_value={"data": 999})
    from app import fetch_data
    result = pytest.run(asyncio.run(fetch_data()))
    assert result == {"data": 999}
```

Or simply in async pytest tests:

```python
@pytest.mark.asyncio
async def test_async_fetch(mocker):
    mocker.patch("app.fetch_data", new_callable=AsyncMock, return_value={"data": 999})
    from app import fetch_data
    result = await fetch_data()
    assert result == {"data": 999}
```

---

## 15. Summary Table

| Technique        | Description                             | Example                               |
| ---------------- | --------------------------------------- | ------------------------------------- |
| `mocker.patch()` | Temporarily replace a function/class    | `mocker.patch("app.requests.get")`    |
| `.return_value`  | Define the mocked return                | `mock.return_value = 200`             |
| `.side_effect`   | Simulate exceptions or multiple results | `mock.side_effect = Exception()`      |
| `mocker.Mock()`  | Create standalone mock objects          | `mock_api = mocker.Mock()`            |
| `mocker.spy()`   | Observe real method calls               | `mocker.spy(obj, "method")`           |
| `mock_open()`    | Simulate file operations                | `patch("builtins.open", mock_open())` |
| `AsyncMock`      | Mock async functions                    | `new_callable=AsyncMock`              |

---

## 16. Conceptual Summary

**Mocking** is about **controlling your test environment**.
It helps ensure your tests:

* Are **fast** (no real API or I/O).
* Are **deterministic** (no randomness or network variance).
* Test only **your logic**, not dependencies.

Think of mocks as *actors pretending to be real services* so your tests focus purely on how your code behaves when interacting with them.

---
