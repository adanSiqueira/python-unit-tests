Lets explore **what fixtures are**, **how they work**, and **why they are so central to pytest**.
Let’s go step by step — from theory to practice, including examples of more advanced uses.

---

## 1. What is a `pytest.fixture`?

In pytest, a **fixture** is a **reusable piece of setup code** that can be shared across multiple tests.

They are used to:

* Prepare **test data**, **objects**, or **resources** (like a database connection, an API client, or a temporary file).
* Provide **clean, isolated test environments** for each test run.
* Handle **setup** and **teardown** logic in a **clean, declarative way**.

So instead of repeating initialization logic in every test, you define it once in a fixture and *inject it* automatically into any test that declares it as a function parameter.

---

## 2. How pytest knows to use it

Pytest automatically looks for **function arguments that match fixture names**.

In your example:

```python
@pytest.fixture
def user_manager():
    """Creates a fresh instance of UserManager for each test"""
    return UserManager()
```

and then:

```python
def test_add_user(user_manager):
    ...
```

Here:

* `pytest` detects that `test_add_user()` has a parameter called `user_manager`
* It looks for a fixture named `user_manager`
* It **calls the fixture first**, gets its return value (a `UserManager` instance),
  and **injects that value** into the test function

So you don’t call the fixture directly — pytest *injects* it automatically based on the parameter name.

---

##  3. What happens behind the scenes

1. When pytest runs your test suite, it scans for fixtures defined with `@pytest.fixture`.
2. It builds a **dependency graph** of which fixtures depend on which others.
3. Before each test, pytest looks at its parameters and injects all required fixtures.
4. After the test finishes, pytest cleans up (runs any teardown logic if defined).

---

## 4. Your Example, Explained

```python
@pytest.fixture
def user_manager():
    """Creates a fresh instance of UserManager for each test"""
    return UserManager()
```

* Creates a **new instance** of `UserManager` for every test.
* Ensures **test isolation** — one test can’t affect another by modifying shared state.

Each test that includes `user_manager` in its signature will get its own **independent** object.

✅ Good practice: fixtures should return *fresh, independent objects* unless explicitly shared (see `scope` below).

---

## 5. Fixture Scopes

By default, each fixture has `scope="function"`, meaning:

* A new fixture instance is created **for each test function**.

You can customize the scope:

| Scope                | Lifetime                                                                           |
| -------------------- | ---------------------------------------------------------------------------------- |
| `function` (default) | Re-created for each test function                                                  |
| `class`              | One instance per test class                                                        |
| `module`             | One instance shared across all tests in a module                                   |
| `package`            | One instance shared across all tests in a package (rare)                           |
| `session`            | One instance shared across the entire test session (often used for DB connections) |

Example:

```python
@pytest.fixture(scope="module")
def db_connection():
    print("Connecting to DB...")
    conn = connect_to_database()
    yield conn
    print("Closing connection...")
    conn.close()
```

### Explanation

* The `yield` keyword allows you to separate **setup** (before `yield`) and **teardown** (after `yield`) logic.
* The code after `yield` runs automatically **after the test (or scope) finishes**, even if the test fails.

---

### 6. Using `yield` for setup/teardown

A fixture can both **prepare** and **clean up** resources:

```python
import tempfile
import os
import pytest

@pytest.fixture
def temp_file():
    # Setup
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"Temporary content")
    f.close()

    yield f.name  # Pass the file path to the test

    # Teardown
    os.remove(f.name)
```

Usage:

```python
def test_file_exists(temp_file):
    assert os.path.exists(temp_file)
```

Even if the test fails, `os.remove()` still executes — pytest ensures proper cleanup.

---

## 7. Fixtures Depending on Other Fixtures

Fixtures can **use other fixtures** — just by declaring them as arguments.

```python
@pytest.fixture
def user_manager():
    return UserManager()

@pytest.fixture
def prepopulated_user_manager(user_manager):
    user_manager.add_user("john_doe", "john@example.com")
    return user_manager

def test_existing_user(prepopulated_user_manager):
    assert prepopulated_user_manager["john_doe"] == "john@example.com"
```

Here, `prepopulated_user_manager` *depends* on `user_manager`.
Pytest automatically injects and resolves dependencies in the correct order.

---

## 8. Fixture Reuse Across Files (conftest.py)

You can define fixtures in a special file named **`conftest.py`** (placed in the root or subfolder of your tests).

Any test file in that directory (or its subdirectories) can automatically use those fixtures **without importing** them.

Example directory:

```
project/
├── app/
│   └── main.py
└── tests/
    ├── conftest.py
    └── test_main.py
```

`conftest.py`:

```python
import pytest
from app.main import UserManager

@pytest.fixture
def user_manager():
    return UserManager()
```

Now `test_main.py` can simply use `user_manager` without importing it.

---

## 9. Parameterized Fixtures

Sometimes you want to run the same test with different fixture configurations.

```python
@pytest.fixture(params=["admin", "editor", "viewer"])
def user_role(request):
    return request.param

def test_roles(user_role):
    assert user_role in ["admin", "editor", "viewer"]
```

This runs the test **three times**, one for each role.

---

## 10. Autouse Fixtures

Fixtures can also run automatically for all tests — even if not explicitly requested.

```python
@pytest.fixture(autouse=True)
def cleanup_environment():
    print("Cleaning test environment...")
```

This fixture executes **before every test** automatically — useful for global cleanup or logging setup.

---

## 11. Fixtures vs Other Testing Structures

Let’s compare with similar structures or patterns:

| Pattern                                    | Description                                                 | When to Use                         |
| ------------------------------------------ | ----------------------------------------------------------- | ----------------------------------- |
| **`@pytest.fixture`**                      | Reusable setup/teardown for multiple tests                  | Common case                         |
| **`setup_function` / `teardown_function`** | Old-style test setup/teardown (works but less modular)      | Legacy tests                        |
| **`setup_method` / `teardown_method`**     | Same as above, for classes                                  | Simple class-based tests            |
| **`unittest.setUp` / `tearDown`**          | xUnit style (in `unittest` framework)                       | When using `unittest` not `pytest`  |
| **`pytest.mark.usefixtures`**              | Force certain fixtures to run even if not explicitly passed | Global behaviors (logging, mocking) |

Example:

```python
@pytest.mark.usefixtures("cleanup_environment")
class TestSomething:
    def test_foo(self):
        ...
```

---

## 12. Real-World Example: Database Testing

A more advanced real-world fixture example:

```python
@pytest.fixture(scope="session")
def db():
    # Setup
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # tests use this

    # Teardown
    session.close()
    engine.dispose()
```

This fixture:

* Creates a temporary in-memory SQLite DB
* Yields a session for tests to use
* Closes and disposes of the engine at the end

Then your tests can depend on it easily:

```python
def test_insert_user(db):
    new_user = User(username="test")
    db.add(new_user)
    db.commit()
    assert db.query(User).filter_by(username="test").first()
```

---

## 13. Summary

| Concept                    | Description                                                             |
| -------------------------- | ----------------------------------------------------------------------- |
| **Fixture**                | Reusable setup and teardown logic                                       |
| **Scope**                  | Controls lifetime of fixture (`function`, `class`, `module`, `session`) |
| **`yield`**                | Separates setup and teardown                                            |
| **Fixture dependencies**   | Fixtures can use other fixtures                                         |
| **`conftest.py`**          | Centralized place for shared fixtures                                   |
| **Parameterized fixtures** | Run tests multiple times with different inputs                          |
| **Autouse fixtures**       | Automatically executed for every test                                   |

---

## Final Notes

Fixtures are one of pytest’s **most powerful features**.
They encourage **clean, DRY, modular testing** by:

* Removing repetitive setup code
* Guaranteeing isolation
* Managing resources safely
* Supporting hierarchical dependencies

They can also integrate seamlessly with **mocking**, **databases**, **temporary directories**, **async tests**, and more.

---

# Async Fixtures in Pytest

When writing tests for asynchronous code (like `async def` functions), you often need your fixtures to also support async setup and teardown.
##  Why Async Fixtures?

When your code uses `async def` functions (like in FastAPI routes, async database calls, or async services),
you also need your **fixtures to support async setup and teardown**.

For example:

* Setting up an async database connection
* Creating async mock clients
* Initializing FastAPI test clients (which are also async)
* Awaiting cleanup after the test

Pytest supports this via **`pytest-asyncio`**, an official plugin.

---

## 2. Setup — Install `pytest-asyncio`

You need to install it:

```bash
pip install pytest-asyncio
```

Then enable it automatically by adding this line to your `pytest.ini` (optional but recommended):

```ini
[pytest]
asyncio_mode = auto
```

That ensures pytest can automatically run async tests and fixtures.

---

## 3. Simple Async Fixture Example

Let’s rewrite your example with async behavior.

### `main.py`

```python
import asyncio

class AsyncUserManager:
    def __init__(self):
        self.users = {}

    async def add_user(self, username, email):
        await asyncio.sleep(0.1)  # simulate async I/O
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = email
        return True

    async def get_user(self, username):
        await asyncio.sleep(0.1)
        return self.users.get(username)
```

### `test_main.py`

```python
import pytest
from main import AsyncUserManager

@pytest.fixture
async def async_user_manager():
    """Creates a fresh instance of AsyncUserManager asynchronously"""
    # Async setup (if needed)
    manager = AsyncUserManager()
    yield manager
    # Async teardown (if needed)
    await asyncio.sleep(0.1)
```

### Tests

```python
@pytest.mark.asyncio
async def test_add_user(async_user_manager):
    assert await async_user_manager.add_user("john_doe", "john@example.com") is True
    assert await async_user_manager.get_user("john_doe") == "john@example.com"

@pytest.mark.asyncio
async def test_add_existing_user(async_user_manager):
    await async_user_manager.add_user("john_doe", "john@example.com")
    with pytest.raises(ValueError):
        await async_user_manager.add_user("john_doe", "another@example.com")

@pytest.mark.asyncio
async def test_get_nonexistent_user(async_user_manager):
    assert await async_user_manager.get_user("ghost") is None
```

**Explanation**

* `@pytest.mark.asyncio` marks the test function as async.
* The async fixture `async_user_manager()` can use `await` inside.
* Both the setup and teardown phases support `await`.

---

## 4. Async Fixture Lifecycle (Setup + Teardown)

Async fixtures can also use `yield`, just like sync fixtures:

```python
@pytest.fixture
async def db_connection():
    conn = await connect_to_db()
    yield conn
    await conn.close()
```

Pytest runs:

1. Everything before `yield` → during setup
2. Everything after `yield` → during teardown, even if tests fail

Example with explicit teardown:

```python
@pytest.fixture
async def temp_data():
    print("Setting up async resource")
    await asyncio.sleep(0.1)
    yield {"data": [1, 2, 3]}
    print("Tearing down async resource")
    await asyncio.sleep(0.1)
```

---

## 5. Combining Sync + Async Fixtures

Pytest is smart enough to mix sync and async fixtures in the same dependency chain.

Example:

```python
@pytest.fixture
def base_config():
    return {"db_url": "sqlite+aiosqlite:///:memory:"}

@pytest.fixture
async def async_db(base_config):
    engine = await async_create_engine(base_config["db_url"])
    yield engine
    await engine.dispose()
```

You can then use both in the same test seamlessly.

---

## 6. Example: FastAPI + Async Fixtures

This is where async fixtures really shine.

### `app.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}
```

### `test_app.py`

```python
import pytest
from httpx import AsyncClient
from app import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_hello(async_client):
    response = await async_client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}
```

 **What’s happening**

* `AsyncClient` is an async HTTP client.
* The `async_client` fixture opens a session and yields it.
* Pytest ensures cleanup (closing the client) after the test finishes.

This pattern is used in *almost every FastAPI test suite*.

---

##  7. Fixture Scope in Async Contexts

The same scopes (`function`, `class`, `module`, `session`) still apply to async fixtures.

Example: One shared database connection across all tests:

```python
@pytest.fixture(scope="session")
async def global_db():
    db = await async_connect()
    yield db
    await db.close()
```

---

## 8. Combining Fixtures and Dependency Injection

Async fixtures can depend on each other:

```python
@pytest.fixture
async def db():
    conn = await async_connect()
    yield conn
    await conn.close()

@pytest.fixture
async def user_repo(db):
    return UserRepository(db)

@pytest.mark.asyncio
async def test_create_user(user_repo):
    user = await user_repo.create_user("john", "john@example.com")
    assert user.email == "john@example.com"
```

Pytest automatically builds the dependency tree, waiting (`await`) as needed.

---

## 9. Advanced: Using `pytest_asyncio.fixture`

You might also see this variant:

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def my_fixture():
    ...
```

It’s identical to `@pytest.fixture` when using `asyncio_mode=auto`,
but explicit usage helps linters and IDEs recognize async behavior better.

---

## 10. Common Gotchas

| Issue                                                        | Cause                                                 | Fix                               |
| ------------------------------------------------------------ | ----------------------------------------------------- | --------------------------------- |
| “RuntimeError: Task got Future attached to a different loop” | Using async fixtures with old pytest-asyncio versions | Upgrade `pytest-asyncio` (≥ 0.21) |
| Fixture not awaited                                          | Forgot `@pytest.mark.asyncio` on test                 | Add it or use `asyncio_mode=auto` |
| Async fixture not running teardown                           | Forgot `yield` inside fixture                         | Use `yield`, not `return`         |

---

##  Summary Table

| Concept                       | Example                                               | Purpose                         |
| ----------------------------- | ----------------------------------------------------- | ------------------------------- |
| **Async fixture**             | `@pytest.fixture async def resource(): ...`           | Support async setup/teardown    |
| **Async test**                | `@pytest.mark.asyncio async def test_x(): ...`        | Run async test functions        |
| **`yield` in async fixture**  | `yield resource` then `await cleanup()`               | Proper async teardown           |
| **Mix sync + async fixtures** | Sync fixture returning config, async fixture using it | Common hybrid setup             |
| **`pytest_asyncio.fixture`**  | Explicit async fixture decorator                      | Alternative form, same behavior |

---

##  Bonus: Real-World Example (Async SQLAlchemy + FastAPI)

Here’s what you might use in a production-like FastAPI project:

```python
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import async_engine, get_session
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture(scope="session")
async def test_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(async_engine) as session:
        yield session
    await async_engine.dispose()

@pytest.fixture
async def client(test_db):
    app.dependency_overrides[get_session] = lambda: test_db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
```

Then:

```python
@pytest.mark.asyncio
async def test_create_user(client):
    res = await client.post("/users", json={"username": "john"})
    assert res.status_code == 201
```

 You’re now combining **async fixtures**, **dependency injection**, and **FastAPI testing**.

---

